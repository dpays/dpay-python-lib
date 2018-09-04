# dPayLib (Python)

This library is unmaintained, do not build productive buisness with it!
Please not the disclaimer in the license file!


Python Library for dPay
========================

Python 3 library for dPay!

Installation
------------

Install with `pip3`:

    $ sudo apt-get install libffi-dev libssl-dev python-dev python3-pip
    $ pip3 install dpay-lib

Manual installation:

    $ git clone https://github.com/dpays/dpay-python-lib/
    $ cd dpay-python-lib
    $ python3 setup.py install --user

Upgrade
-------

    $ pip3 install dpay --user --upgrade

Additional dependencies
-----------------------

`dpayapi.dpayasyncclient`:
 * `asyncio==3.4.3`
 * `pyyaml==3.11`

Documentation
-------------

Documentation is written with the help of sphinx and can be compile to
html with:

    cd docs
    make html
