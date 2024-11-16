from p2pnetwork.node import Node
from PeerDiscoveryHandler import PeerDiscoveryHandler
from SocketConnector import SocketConnector
from BlockchainUtils import BlockchainUtils
import json


class SocketCommunication(Node):
    # Class responsible for managing communication between nodes in the P2P network

    def __init__(self, ip, port):
        """
        Initializes the SocketCommunication class, setting up the peer discovery handler
        and socket connector for communication with other nodes.

        :param ip: The IP address of the node.
        :param port: The port number of the node.
        """
        super(SocketCommunication, self).__init__(ip, port, None)  # Initializes the P2P node with the given IP and port
        self.peers = []  # List to store connected peers
        self.peerDiscoveryHandler = PeerDiscoveryHandler(self)  # Peer discovery handler to manage peer connections
        self.socketConnector = SocketConnector(ip, port)  # Socket connector for communication with other nodes

    def connectToFirstNode(self):
        """
        Connects to the first node (genesis node) if the current node is not the default one.
        By default, connects to the node at 'localhost' on port 10001.
        """
        if self.socketConnector.port != 10001:
            self.connect_with_node('localhost', 10001)  # Connects to the genesis node at port 10001

    def startSocketCommunication(self, node):
        """
        Starts the socket communication by initializing the node and beginning the peer discovery process.
        
        :param node: The current node to be initialized and connected.
        """
        self.node = node  # Assign the current node
        self.start()  # Starts the node
        self.peerDiscoveryHandler.start()  # Starts the peer discovery handler
        self.connectToFirstNode()  # Connects to the first node (genesis node)

    def inbound_node_connected(self, connected_node):
        """
        Handles the connection of an inbound node (a node trying to connect to this node).

        :param connected_node: The node that has connected inbound.
        """
        self.peerDiscoveryHandler.handshake(connected_node)  # Performs a handshake with the connected node

    def outbound_node_connected(self, connected_node):
        """
        Handles the connection of an outbound node (this node trying to connect to another node).

        :param connected_node: The node that has been connected outbound.
        """
        self.peerDiscoveryHandler.handshake(connected_node)  # Performs a handshake with the connected node

    def node_message(self, connected_node, message):
        """
        Handles messages received from other nodes. Based on the message type, it takes different actions.

        :param connected_node: The node from which the message was received.
        :param message: The message that was received from the connected node.
        """
        message = BlockchainUtils.decode(json.dumps(message))  # Decodes the received message into a proper format
        if message.messageType == 'DISCOVERY':
            self.peerDiscoveryHandler.handleMessage(message)  # Handles discovery message to update peer list
        elif message.messageType == 'TRANSACTION':
            transaction = message.data  # Extracts transaction data from the message
            self.node.handleTransaction(transaction)  # Handles the received transaction
        elif message.messageType == 'BLOCK':
            block = message.data  # Extracts block data from the message
            self.node.handleBlock(block)  # Handles the received block
        elif message.messageType == 'BLOCKCHAINREQUEST':
            self.node.handleBlockchainRequest(connected_node)  # Responds to a blockchain request from a node
        elif message.messageType == 'BLOCKCHAIN':
            blockchain = message.data  # Extracts blockchain data from the message
            self.node.handleBlockchain(blockchain)  # Handles the received blockchain

    def send(self, receiver, message):
        """
        Sends a message to a specific node.

        :param receiver: The target node to receive the message.
        :param message: The message to be sent.
        """
        self.send_to_node(receiver, message)  # Sends the message to the specified receiver node

    def broadcast(self, message):
        """
        Broadcasts a message to all connected nodes.

        :param message: The message to be broadcasted.
        """
        self.send_to_nodes(message)  # Sends the message to all connected nodes in the network
