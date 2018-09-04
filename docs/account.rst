Account
~~~~~~~

Obtaining data of an account.

.. code-block:: python

   from dpaypy.account import Account
   account = Account("jared")
   print(account)
   print(account.reputation())
   print(account.balances)

.. autoclass:: dpaypy.account.Account
   :members:
