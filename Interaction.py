from Wallet import Wallet  # Importing the Wallet class
from BlockchainUtils import BlockchainUtils  # Importing blockchain utility functions
import requests  # Importing the requests library for HTTP requests

def postTransaction(sender, receiver, amount, type):
    """
    Creates and sends a transaction from a sender to a receiver.

    :param sender: The wallet initiating the transaction
    :param receiver: The wallet receiving the transaction
    :param amount: The transaction amount
    :param type: The type of transaction (e.g., EXCHANGE, STAKE, TRANSFER)
    """
    # Create a transaction using the sender's wallet
    transaction = sender.createTransaction(receiver.publicKeyString(), amount, type)
    url = "http://localhost:5000/transaction"  # API endpoint to send the transaction
    package = {'transaction': BlockchainUtils.encode(transaction)}  # Package the transaction as a dictionary
    request = requests.post(url, json=package)  # Send the transaction to the server

if __name__ == '__main__':
    # Initialize wallets for Bob and Alice
    bob = Wallet()  # Creating Bob's wallet
    alice = Wallet()  # Creating Alice's wallet
    alice.fromKey('keys/stakerPrivateKey.pem')  # Load Alice's private key from a file
    exchange = Wallet()  # Creating a wallet for the exchange

    # Sending transactions using the exchange wallet
    # Forger: genesis
    postTransaction(exchange, alice, 100, 'EXCHANGE')  # Transfer 100 to Alice
    postTransaction(exchange, bob, 100, 'EXCHANGE')  # Transfer 100 to Bob
    postTransaction(exchange, bob, 10, 'EXCHANGE')   # Transfer 10 to Bob

    # Sending transactions using Alice's wallet
    # Forger: likely Alice
    postTransaction(alice, alice, 25, 'STAKE')  # Alice stakes 25
    postTransaction(alice, bob, 1, 'TRANSFER')   # Alice transfers 1 to Bob
    postTransaction(alice, bob, 1, 'TRANSFER')   # Alice transfers another 1 to Bob
