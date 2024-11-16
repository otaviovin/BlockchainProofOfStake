import uuid
import time
import copy

class Transaction():
    """
    This class represents a financial or blockchain transaction, which includes information
    about the sender, receiver, amount, transaction type, unique ID, timestamp, and signature.
    """

    def __init__(self, senderPublicKey, receiverPublicKey, amount, type):
        """
        Initializes a new transaction with the given parameters.

        :param senderPublicKey: Public key of the sender
        :param receiverPublicKey: Public key of the receiver
        :param amount: The amount to be transferred in the transaction
        :param type: Type of transaction (e.g., transfer, exchange)
        """
        self.senderPublicKey = senderPublicKey  # Public key of the sender
        self.receiverPublicKey = receiverPublicKey  # Public key of the receiver
        self.amount = amount  # Amount to be transferred in the transaction
        self.type = type  # Type of transaction (e.g., transfer, swap, etc.)
        self.id = (uuid.uuid1()).hex  # Unique transaction ID generated using UUID1 (based on timestamp and MAC address)
        self.timestamp = time.time()  # Timestamp of the transaction creation, representing the time in seconds since the epoch
        self.signature = ''  # Placeholder for the transaction's signature (initially empty)

    def toJson(self):
        """
        Converts the transaction object to a dictionary representation suitable for JSON serialization.

        :return: A dictionary containing the transaction's data
        """
        return self.__dict__  # Returns the transaction object as a dictionary (JSON format)

    def sign(self, signature):
        """
        Adds a signature to the transaction to validate it.

        :param signature: The signature to attach to the transaction
        """
        self.signature = signature  # Assign the given signature to the transaction

    def payload(self):
        """
        Creates and returns the payload of the transaction. The payload is the transaction data 
        without the signature, so it can be used for verification or broadcasting.

        :return: A dictionary representation of the transaction without the signature
        """
        jsonRepresentation = copy.deepcopy(self.toJson())  # Create a copy of the transaction data
        jsonRepresentation['signature'] = ''  # Remove the signature from the copied data to generate the payload
        return jsonRepresentation  # Return the transaction data without the signature

    def equals(self, transaction):
        """
        Compares the current transaction with another transaction to check if they are equal.

        :param transaction: Another transaction object to compare with
        :return: True if the transactions have the same ID, otherwise False
        """
        return self.id == transaction.id  # Returns True if the transaction IDs match, indicating equality
