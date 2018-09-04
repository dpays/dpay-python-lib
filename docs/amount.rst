Amount
~~~~~~

For the sake of easier handling of Assets on the blockchain

.. code-block:: python

   from dpaypy.amount import Amount
   a = Amount("1 BBD")
   b = Amount("20 BBD")
   a + b
   a * 2
   a += b
   a /= 2.0

.. autoclass:: dpaypy.amount.Amount
   :members:
