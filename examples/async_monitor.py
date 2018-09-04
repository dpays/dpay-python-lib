from dpay.utils import parse_time

try:
    import asyncio
except ImportError:
    raise ImportError("Missing dependency: asyncio")

try:
    import aiohttp
except ImportError:
    raise ImportError("Missing dependency: aiohttp")

from dpayapi.dpayasyncclient import DPayAsyncClient, Config
import re

account = "witness-account"  # Replace with  account you wish to monitor

re_asset = re.compile(r'(?P<number>\d*\.?\d+)\s?(?P<unit>[a-zA-Z]+)')


def read_asset(asset_string):
    res = re_asset.match(asset_string)
    return {'value': float(res.group('number')), 'symbol': res.group('unit')}


def read_time(time_string):
    return int(parse_time(time_string).timestamp())


@asyncio.coroutine
def get_dpay_price(sess):
    response = yield from sess.get("https://coinmarketcap-nexuist.rhcloud.com/api/bex")
    ret = yield from response.json()
    return ret["price"]["usd"]


@asyncio.coroutine
def get_witness_price_feed(dpay, acct):
    r = yield from dpay.wallet.get_witness(acct)
    last_update_time = read_time(r["last_bbd_exchange_update"])
    p = r["bbd_exchange_rate"]
    last_price = read_asset(p["base"])["value"] / read_asset(p["quote"])["value"]
    return (last_update_time, last_price)


@asyncio.coroutine
def start(dpay):
    with aiohttp.ClientSession() as session:
        futures = {"time": None, "exchange_price": None, "witness_price": None, "db": None}
        last_witness_update_time, last_witness_price = yield from get_witness_price_feed(dpay, account)
        r = yield from dpay.db.get_dynamic_global_properties()
        last_time = read_time(r["time"])
        cur_time = last_time
        first_time = True
        dpay_price = yield from get_dpay_price(session)
        futures["time"] = asyncio.async(asyncio.sleep(0))
        needs_updating = False
        while True:
            ftrs = []
            for f in futures.values():
                if f:
                    ftrs.append(f)
            done, pending = yield from asyncio.wait(ftrs, return_when=asyncio.FIRST_COMPLETED)

            old_futures = {}
            for k, f in futures.items():
                old_futures[k] = futures[k]
            for k, f in old_futures.items():
                if f in done:
                    futures[k] = None
                    if k == "time":
                        futures["time"] = asyncio.async(asyncio.sleep(3))
                        if futures["db"]:
                            futures["db"].cancel()
                        futures["db"] = yield from dpay.db.get_dynamic_global_properties(future=True)
                    elif k == "exchange_price":
                        dpay_price = f.result()
                        if abs(1 - last_witness_price / dpay_price) > 0.03 and (cur_time - last_witness_update_time) > 60 * 60:
                            if not needs_updating:
                                needs_updating = True
                                print("Price feed needs to be updated due to change in price.")
                                print("Current witness price: {} $/BEX   Current exchange price: {} $/BEX".format(last_witness_price, dpay_price))
                        else:
                            if needs_updating and cur_time - last_witness_update_time < 24 * 60 * 60:
                                needs_updating = False
                                print("Price feed no longer needs to be updated")

                    elif k == "witness_price":
                        new_last_witness_update_time, new_last_witness_price = f.result()
                        if new_last_witness_update_time != last_witness_update_time:
                            last_witness_update_time = new_last_witness_update_time
                            last_witness_price = new_last_witness_price
                            print("Price feed has been updated")
                            needs_updating = False
                    elif k == "db":
                        r = f.result()
                        cur_time = read_time(r["time"])
                        if first_time or cur_time - last_time > 28:  # seconds
                            first_time = False
                            print("Block number {} at time: {}".format(r["head_block_number"], r["time"]))
                            if needs_updating:
                                print("Price feed still needs updating to {} $/BEX".format(dpay_price))
                            futures["exchange_price"] = asyncio.async(get_dpay_price(session))
                            futures["witness_price"] = asyncio.async(get_witness_price_feed(dpay, account))
                            last_time = cur_time
                        if cur_time - last_witness_update_time >= 24 * 60 * 60:
                            if not needs_updating:
                                needs_updating = True
                                print("Price feed needs to be updated because it is too old.")
            old_futures = {}


if __name__ == "__main__":
    dpay = DPayAsyncClient(Config(config_file="async_monitor_config.yml"))
    dpay.run([start])  # If multiple coroutines were specified in the array, they would run concurrently
