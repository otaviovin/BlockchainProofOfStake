from Crypto.PublicKey import RSA  # Importing RSA key generation and management functions
from Transaction import Transaction  # Importing the Transaction class to create and manage transactions
from Block import Block  # Importing the Block class to create and manage blocks
from BlockchainUtils import BlockchainUtils  # Importing utility functions for blockchain-related tasks
from Crypto.Signature import PKCS1_v1_5  # Importing the RSA signature scheme used for signing and verifying data

class Wallet():
    """
    The Wallet class represents a digital wallet that can generate key pairs, sign data, 
    create transactions, and manage blocks. It uses RSA for cryptographic operations.
    """

    def __init__(self):
        """
        Initializes the wallet by generating a new RSA key pair.
        The key pair will be used for signing transactions and blocks.
        """
        self.keyPair = RSA.generate(2048)  # Generates a new RSA key pair of 2048 bits for the wallet

    def fromKey(self, file):
        """
        Loads an RSA key pair from a file.

        :param file: The path to the file containing the RSA private key
        """
        key = ''
        with open(file, 'r') as keyfile:
            key = RSA.importKey(keyfile.read())  # Imports the RSA key from the specified file
        self.keyPair = key  # Sets the key pair of the wallet to the imported key

    def sign(self, data):
        """
        Signs the given data using the wallet's private key.

        :param data: The data to be signed
        :return: The signature in hexadecimal format
        """
        dataHash = BlockchainUtils.hash(data)  # Generates the hash of the data to be signed
        signatureSchemeObject = PKCS1_v1_5.new(self.keyPair)  # Initializes the RSA signature scheme using the private key
        signature = signatureSchemeObject.sign(dataHash)  # Signs the hash of the data
        return signature.hex()  # Returns the signature in hexadecimal format for easier storage and transmission

    @staticmethod
    def signatureValid(data, signature, publicKeyString):
        """
        Verifies the validity of a signature using a public key.

        :param data: The data that was signed
        :param signature: The signature to be verified (in hexadecimal format)
        :param publicKeyString: The public key in string format (PEM)
        :return: True if the signature is valid, otherwise False
        """
        signature = bytes.fromhex(signature)  # Converts the hexadecimal signature back into bytes
        dataHash = BlockchainUtils.hash(data)  # Generates the hash of the data to be verified
        publicKey = RSA.importKey(publicKeyString)  # Imports the public key from the provided string (PEM format)
        signatureSchemeObject = PKCS1_v1_5.new(publicKey)  # Initializes the RSA signature scheme using the public key
        signatureValid = signatureSchemeObject.verify(dataHash, signature)  # Verifies the signature against the data hash
        return signatureValid  # Returns True if the signature is valid, otherwise False

    def publicKeyString(self):
        """
        Exports the wallet's public key as a PEM-encoded string.

        :return: The public key in PEM format as a string
        """
        publicKeyString = self.keyPair.publickey().exportKey('PEM').decode('utf-8')  # Exports the public key in PEM format
        return publicKeyString  # Returns the public key as a string

    def createTransaction(self, receiver, amount, type):
        """
        Creates a new transaction, signs it, and returns the signed transaction.

        :param receiver: The public key of the transaction receiver
        :param amount: The amount to be transferred
        :param type: The type of transaction (e.g., 'transfer', 'swap')
        :return: The signed transaction object
        """
        transaction = Transaction(self.publicKeyString(), receiver, amount, type)  # Creates a new transaction
        signature = self.sign(transaction.payload())  # Signs the transaction payload (without signature)
        transaction.sign(signature)  # Adds the signature to the transaction
        return transaction  # Returns the signed transaction

    def createBlock(self, transactions, lastHash, blockCount):
        """
        Creates a new block containing the given transactions, signs it, and returns the signed block.

        :param transactions: The list of transactions to include in the block
        :param lastHash: The hash of the previous block (used to link blocks)
        :param blockCount: The block number (or height) of the new block
        :return: The signed block object
        """
        block = Block(transactions, lastHash, self.publicKeyString(), blockCount)  # Creates a new block with the given parameters
        signature = self.sign(block.payload())  # Signs the block payload (without signature)
        block.sign(signature)  # Adds the signature to the block
        return block  # Returns the signed block
