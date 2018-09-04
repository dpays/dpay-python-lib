Transaction Builder
~~~~~~~~~~~~~~~~~~~

To build your own transactions and sign them

.. code-block:: python

   from dpaypy.transactionbuilder import TransactionBuilder
   from dpaypybase.operations import Vote
   tx = TransactionBuilder()
   tx.appendOps(Vote(
       **{"voter": voter,
          "author": post_author,
          "permlink": post_permlink,
          "weight": int(weight * DPAY_1_PERCENT)}  # DPAY_1_PERCENT = 100
   ))
   tx.appendSigner("jared", "posting")
   tx.sign()
   tx.broadcast()

.. autoclass:: dpaypy.transactionbuilder.TransactionBuilder
   :members:
