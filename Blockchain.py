from Block import Block  # Imports the Block class
from BlockchainUtils import BlockchainUtils  # Imports utilities for blockchain operations
from AccountModel import AccountModel  # Imports the account management system
from ProofOfStake import ProofOfStake  # Imports the Proof-of-Stake system

class Blockchain():
    def __init__(self):
        """
        Initializes a new instance of the blockchain.

        The constructor sets up the genesis block, an account model for balance management,
        and a Proof of Stake (PoS) system to determine block forgers.
        """
        self.blocks = [Block.genesis()]  # Creates a list of blocks starting with the genesis block
        self.accountModel = AccountModel()  # Initializes the account model for managing balances
        self.pos = ProofOfStake()  # Sets up the Proof-of-Stake mechanism

    def addBlock(self, block):
        """
        Adds a new block to the blockchain and executes its transactions.

        :param block: The block to be added
        """
        self.executeTransactions(block.transactions)  # Executes the block's transactions
        self.blocks.append(block)  # Appends the block to the blockchain

    def toJson(self):
        """
        Converts the blockchain into a JSON-like dictionary representation.

        :return: A dictionary representing the blockchain
        """
        data = {}
        jsonBlocks = []
        for block in self.blocks:
            jsonBlocks.append(block.toJson())  # Converts each block to JSON and adds it to the list
        data['blocks'] = jsonBlocks  # Stores all blocks in the 'data' dictionary
        return data

    def blockCountValid(self, block):
        """
        Checks if the block count of the proposed block is valid.

        :param block: The block to be validated
        :return: True if the block count is valid, False otherwise
        """
        if self.blocks[-1].blockCount == block.blockCount - 1:
            return True  # Block count is valid
        else:
            return False  # Block count is invalid

    def lastBlockHashValid(self, block):
        """
        Validates the hash of the last block in the blockchain.

        :param block: The block to be validated
        :return: True if the hash is valid, False otherwise
        """
        latestBlockchainBlockHash = BlockchainUtils.hash(
            self.blocks[-1].payload()).hexdigest()  # Calculates the hash of the last block
        if latestBlockchainBlockHash == block.lastHash:
            return True  # Hash matches
        else:
            return False  # Hash does not match

    def getCoveredTransactionSet(self, transactions):
        """
        Filters out transactions that are "covered" (i.e., valid based on the sender's balance).

        :param transactions: The list of transactions to filter
        :return: A list of covered transactions
        """
        coveredTransactions = []
        for transaction in transactions:
            if self.transactionCovered(transaction):
                coveredTransactions.append(transaction)  # Adds covered transaction to the list
            else:
                print('Transaction is not covered by sender')  # Logs invalid transactions
        return coveredTransactions

    def transactionCovered(self, transaction):
        """
        Checks if a transaction is covered by the sender's balance.

        :param transaction: The transaction to validate
        :return: True if the transaction is covered, False otherwise
        """
        if transaction.type == 'EXCHANGE':
            return True  # EXCHANGE transactions are always covered
        senderBalance = self.accountModel.getBalance(transaction.senderPublicKey)  # Gets the sender's balance
        if senderBalance >= transaction.amount:
            return True  # Balance is sufficient
        else:
            return False  # Balance is insufficient

    def executeTransactions(self, transactions):
        """
        Executes a list of transactions by updating account balances.

        :param transactions: The transactions to be executed
        """
        for transaction in transactions:
            self.executeTransaction(transaction)  # Executes each transaction individually

    def executeTransaction(self, transaction):
        """
        Executes a single transaction and updates the balances of the involved accounts.

        :param transaction: The transaction to be executed
        """
        if transaction.type == 'STAKE':
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            if sender == receiver:  # For staking, sender and receiver must be the same account
                amount = transaction.amount
                self.pos.update(sender, amount)  # Updates the stake
                self.accountModel.updateBalance(sender, -amount)  # Deducts the staked amount from the sender's balance
        else:
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            amount = transaction.amount
            self.accountModel.updateBalance(sender, -amount)  # Deducts the amount from the sender
            self.accountModel.updateBalance(receiver, amount)  # Adds the amount to the receiver

    def nextForger(self):
        """
        Determines the next forger of the blockchain based on the PoS system.

        :return: The public key of the next forger
        """
        lastBlockHash = BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest()  # Gets the last block's hash
        nextForger = self.pos.forger(lastBlockHash)  # Determines the next forger
        return nextForger

    def createBlock(self, transactionsFromPool, forgerWallet):
        """
        Creates a new block from available transactions and the forger's wallet.

        :param transactionsFromPool: Transactions available for inclusion in the block
        :param forgerWallet: The wallet of the forger
        :return: The newly created block
        """
        coveredTransactions = self.getCoveredTransactionSet(transactionsFromPool)  # Gets covered transactions
        self.executeTransactions(coveredTransactions)  # Executes the covered transactions
        newBlock = forgerWallet.createBlock(
            coveredTransactions, BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest(), len(self.blocks))
        self.blocks.append(newBlock)  # Adds the new block to the blockchain
        return newBlock

    def transactionExists(self, transaction):
        """
        Checks if a transaction already exists in the blockchain.

        :param transaction: The transaction to check
        :return: True if the transaction exists, False otherwise
        """
        for block in self.blocks:
            for blockTransaction in block.transactions:
                if transaction.equals(blockTransaction):
                    return True  # Transaction exists
        return False  # Transaction does not exist

    def forgerValid(self, block):
        """
        Validates the forger of a proposed block.

        :param block: The block to validate
        :return: True if the forger is valid, False otherwise
        """
        forgerPublicKey = self.pos.forger(block.lastHash)  # Gets the expected forger for the block
        proposedBlockForger = block.forger  # Gets the forger proposed in the block
        if forgerPublicKey == proposedBlockForger:
            return True  # Forger is valid
        else:
            return False  # Forger is invalid

    def transactionsValid(self, transactions):
        """
        Validates a set of transactions to ensure they are covered.

        :param transactions: The transactions to validate
        :return: True if all transactions are valid, False otherwise
        """
        coveredTransactions = self.getCoveredTransactionSet(transactions)  # Gets covered transactions
        if len(coveredTransactions) == len(transactions):
            return True  # All transactions are covered
        return False  # Some transactions are not covered
