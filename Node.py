from Blockchain import Blockchain
from TransactionPool import TransactionPool
from Wallet import Wallet
from SocketCommunication import SocketCommunication
from NodeAPI import NodeAPI
from Message import Message
from BlockchainUtils import BlockchainUtils
import copy


class Node():

    def __init__(self, ip, port, key=None):
        """
        Initializes a Node instance with connection parameters and optionally a key.

        :param ip: The IP address of the node
        :param port: The port number of the node
        :param key: Optional private key for the node's wallet
        """
        self.p2p = None  # Peer-to-peer communication component (not initialized)
        self.ip = ip  # IP address of the node
        self.port = port  # Port number of the node
        self.blockchain = Blockchain()  # Initializes the blockchain
        self.transactionPool = TransactionPool()  # Initializes the transaction pool
        self.wallet = Wallet()  # Initializes the node's wallet
        if key is not None:  # If a key is provided
            self.wallet.fromKey(key)  # Load the private key into the wallet

    def startP2P(self):
        """
        Starts the P2P communication for the node using its IP and port.
        """
        self.p2p = SocketCommunication(self.ip, self.port)  # Set up P2P communication
        self.p2p.startSocketCommunication(self)  # Begin listening for connections

    def startAPI(self, apiPort):
        """
        Starts the node's API on the specified port.

        :param apiPort: Port number for the API
        """
        self.api = NodeAPI()  # Create a new Node API instance
        self.api.injectNode(self)  # Inject the node instance into the API
        self.api.start(apiPort)  # Start the API on the specified port

    def handleTransaction(self, transaction):
        """
        Processes a received transaction.

        :param transaction: The transaction to handle
        """
        data = transaction.payload()  # Get the transaction payload
        signature = transaction.signature  # Get the transaction's signature
        signerPublicKey = transaction.senderPublicKey  # Get the sender's public key

        # Validate the signature of the transaction
        signatureValid = Wallet.signatureValid(data, signature, signerPublicKey)
        # Check if the transaction already exists in the pool or the blockchain
        transactionExists = self.transactionPool.transactionExists(transaction)
        transactionInBlock = self.blockchain.transactionExists(transaction)

        if not transactionExists and not transactionInBlock and signatureValid:
            # If the transaction is new and the signature is valid, add it to the pool
            self.transactionPool.addTransaction(transaction)
            message = Message(self.p2p.socketConnector, 'TRANSACTION', transaction)  # Create a transaction message
            encodedMessage = BlockchainUtils.encode(message)  # Encode the message
            self.p2p.broadcast(encodedMessage)  # Broadcast the message to other nodes

            # Check if a new block needs to be forged
            forgingRequired = self.transactionPool.forgingRequired()
            if forgingRequired:
                self.forge()  # Call the forge method to create a block

    def handleBlock(self, block):
        """
        Processes a received block.

        :param block: The block to handle
        """
        forger = block.forger  # Get the block's forger
        blockHash = block.payload()  # Get the block's data for hashing
        signature = block.signature  # Get the block's signature

        # Validate the block
        blockCountValid = self.blockchain.blockCountValid(block)
        lastBlockHashValid = self.blockchain.lastBlockHashValid(block)
        forgerValid = self.blockchain.forgerValid(block)
        transactionsValid = self.blockchain.transactionsValid(block.transactions)
        signatureValid = Wallet.signatureValid(blockHash, signature, forger)

        if not blockCountValid:
            # If the block count is invalid, request the chain
            self.requestChain()
        if lastBlockHashValid and forgerValid and transactionsValid and signatureValid:
            # If the block is valid, add it to the blockchain
            self.blockchain.addBlock(block)
            self.transactionPool.removeFromPool(block.transactions)  # Remove transactions from the pool
            message = Message(self.p2p.socketConnector, 'BLOCK', block)  # Create a block message
            self.p2p.broadcast(BlockchainUtils.encode(message))  # Broadcast the block

    def handleBlockchainRequest(self, requestingNode):
        """
        Handles a request for the blockchain from another node.

        :param requestingNode: The node requesting the blockchain
        """
        message = Message(self.p2p.socketConnector, 'BLOCKCHAIN', self.blockchain)  # Create a blockchain message
        self.p2p.send(requestingNode, BlockchainUtils.encode(message))  # Send the blockchain to the requesting node

    def handleBlockchain(self, blockchain):
        """
        Processes a received blockchain.

        :param blockchain: The blockchain to handle
        """
        localBlockchainCopy = copy.deepcopy(self.blockchain)  # Make a copy of the local blockchain
        localBlockCount = len(localBlockchainCopy.blocks)  # Count local blocks
        receivedChainBlockCount = len(blockchain.blocks)  # Count received chain blocks

        if localBlockCount < receivedChainBlockCount:
            # If the received blockchain is longer, add the new blocks
            for blockNumber, block in enumerate(blockchain.blocks):
                if blockNumber >= localBlockCount:
                    localBlockchainCopy.addBlock(block)  # Add the block to the copy
                    self.transactionPool.removeFromPool(block.transactions)  # Remove transactions from the pool
            self.blockchain = localBlockchainCopy  # Update the local blockchain

    def forge(self):
        """
        Forges a new block if this node is the forger.
        """
        forger = self.blockchain.nextForger()  # Get the next forger
        if forger == self.wallet.publicKeyString():  # Check if this node is the forger
            print('I am the forger')  # Log message
            block = self.blockchain.createBlock(self.transactionPool.transactions, self.wallet)  # Create a new block
            self.transactionPool.removeFromPool(self.transactionPool.transactions)  # Remove transactions from the pool
            message = Message(self.p2p.socketConnector, 'BLOCK', block)  # Create a block message
            self.p2p.broadcast(BlockchainUtils.encode(message))  # Broadcast the block
        else:
            print('I am not the forger')  # Log message if not the forger

    def requestChain(self):
        """
        Requests the blockchain from other nodes.
        """
        message = Message(self.p2p.socketConnector, 'BLOCKCHAINREQUEST', None)  # Create a blockchain request message
        self.p2p.broadcast(BlockchainUtils.encode(message))  # Broadcast the request
