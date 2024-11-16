class TransactionPool():
    """
    The TransactionPool class manages a collection of pending transactions. It allows adding,
    checking, removing, and verifying transactions in the pool, which is typically used to store 
    transactions before they are included in a block.
    """

    def __init__(self):
        """
        Initializes a new transaction pool to hold the pending transactions.
        """
        self.transactions = []  # List to store the pending transactions in the pool

    def addTransaction(self, transaction):
        """
        Adds a new transaction to the transaction pool.

        :param transaction: The transaction object to be added to the pool
        """
        self.transactions.append(transaction)  # Adds the given transaction to the pool

    def transactionExists(self, transaction):
        """
        Checks if a given transaction already exists in the transaction pool.

        :param transaction: The transaction to check for existence in the pool
        :return: True if the transaction is already in the pool, otherwise False
        """
        for poolTransaction in self.transactions:
            if poolTransaction.equals(transaction):  # Checks if the current pool transaction is equal to the given one
                return True  # Returns True if the transaction already exists in the pool
        return False  # Returns False if the transaction is not found in the pool

    def removeFromPool(self, transactions):
        """
        Removes a list of transactions from the transaction pool.

        :param transactions: A list of transactions to be removed from the pool
        """
        newPoolTransactions = []  # A new list to store transactions that will remain in the pool
        for poolTransaction in self.transactions:
            insert = True  # Flag to determine if a transaction should be inserted into the new pool
            for transaction in transactions:
                if poolTransaction.equals(transaction):  # If the pool transaction is in the list of transactions to be removed
                    insert = False  # Mark the transaction to not be added to the new pool
            if insert:
                newPoolTransactions.append(poolTransaction)  # Keep the transaction in the pool if it was not removed
        self.transactions = newPoolTransactions  # Update the pool with the remaining transactions

    def forgingRequired(self):
        """
        Determines if forging (mining or block creation) is required by checking if there are pending transactions.

        :return: True if there is at least one transaction in the pool, otherwise False
        """
        return len(self.transactions) >= 1  # Returns True if there is one or more transactions in the pool
