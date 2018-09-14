from dpayapi.dpaynoderpc import DPayNodeRPC
from pprint import pprint

rpc = DPayNodeRPC("wss://dpayd.dpays.io/ws")

for a in rpc.stream("comment", start=1893850):
    pprint(a)
