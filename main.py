from Transaction import Transaction  # Importing the Transaction class
from Wallet import Wallet  # Importing the Wallet class
from TransactionPool import TransactionPool  # Importing the TransactionPool class
from Block import Block  # Importing the Block class
from Blockchain import Blockchain  # Importing the Blockchain class
import pprint  # Importing pprint for pretty-printing
from BlockchainUtils import BlockchainUtils  # Importing Blockchain utility functions
from AccountModel import AccountModel  # Importing the AccountModel class
from Node import Node  # Importing the Node class
import sys  # Importing sys for command-line argument handling

if __name__ == '__main__':
    """
    Main script execution starts here.
    This script sets up and runs a blockchain node based on the provided command-line arguments.
    """
    print("Starting the script...")  # Notify that the script has started

    # Retrieve command-line arguments to configure the node
    ip = sys.argv[1]  # The IP address of the node
    port = int(sys.argv[2])  # The port for the node
    apiPort = int(sys.argv[3])  # The port for the node's API
    keyFile = None  # Initialize the key file variable as None

    # Check if a key file path was provided as an argument
    if len(sys.argv) > 4:
        keyFile = sys.argv[4]  # If provided, store the path to the key file

    # Create a new instance of the Node class with the provided configuration
    node = Node(ip, port, keyFile)
    
    # Start the node's peer-to-peer (P2P) service
    node.startP2P()
    
    # Start the node's API service on the specified API port
    node.startAPI(apiPort)
