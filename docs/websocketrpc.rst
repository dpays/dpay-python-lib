************
DPayNodeRPC
************

.. warning:: This is a low level class that can be used in combination with
             ``DPayClient``. Do not use this class unless you know what
             you are doing!

This class allows to call API methods exposed by the witness node via
websockets.

Defintion
=========
.. autoclass:: dpaypyapi.dpaynoderpc.DPayNodeRPC
    :members: rpcexec, __getattr__
