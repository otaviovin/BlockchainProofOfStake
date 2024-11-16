import threading
import time
from Message import Message
from BlockchainUtils import BlockchainUtils


class PeerDiscoveryHandler():
    # Class responsible for managing peer discovery and connection status in the network

    def __init__(self, node):
        """
        Initializes the PeerDiscoveryHandler with the provided node instance.

        :param node: The node instance which contains the socket communication for the peer network.
        """
        self.socketCommunication = node  # Stores the node's socket communication instance

    def start(self):
        """
        Starts the threads for monitoring connection status and discovering new peers.

        This method creates and starts two threads: one for checking and printing the status
        of existing connections, and another for broadcasting discovery messages to find new peers.
        """
        statusThread = threading.Thread(target=self.status, args=())  # Creates a thread for monitoring connection status
        statusThread.start()  # Starts the connection status thread
        discoveryThread = threading.Thread(target=self.discovery, args=())  # Creates a thread for peer discovery
        discoveryThread.start()  # Starts the peer discovery thread

    def status(self):
        """
        Monitors and prints the current peer connections every 5 seconds.

        This method runs in a continuous loop, printing the IP and port of each connected peer,
        then waits for 5 seconds before printing again.
        """
        while True:
            print('Current Connections:')
            for peer in self.socketCommunication.peers:
                # Prints the IP and port of each connected peer
                print(str(peer.ip) + ':' + str(peer.port))  
            time.sleep(5)  # Waits for 5 seconds before printing the connection status again

    def discovery(self):
        """
        Sends discovery messages every 10 seconds to find new peers.

        This method broadcasts a handshake message to all known peers at a regular interval of 10 seconds,
        allowing the node to discover new peers in the network.
        """
        while True:
            handshakeMessage = self.handshakeMessage()  # Creates a handshake message for peer discovery
            self.socketCommunication.broadcast(handshakeMessage)  # Broadcasts the handshake message to peers
            time.sleep(10)  # Waits for 10 seconds before sending the next discovery message

    def handshake(self, connected_node):
        """
        Sends a handshake message to a connected node.

        This method is used to send a discovery message to a specific peer node to establish
        or confirm a connection.

        :param connected_node: The peer node to which the handshake message will be sent.
        """
        handshakeMessage = self.handshakeMessage()  # Creates a handshake message for the node
        self.socketCommunication.send(connected_node, handshakeMessage)  # Sends the handshake message to the node

    def handshakeMessage(self):
        """
        Creates and returns an encoded handshake message containing the list of known peers.

        This method gathers the local node's connector and its list of known peers, packages them
        into a message, and encodes the message for transmission to other peers.

        :return: The encoded handshake message.
        """
        ownConnector = self.socketCommunication.socketConnector  # Gets the local node's connector
        ownPeers = self.socketCommunication.peers  # Gets the list of known peers
        data = ownPeers  # Defines the message's data as the list of known peers
        messageType = 'DISCOVERY'  # Defines the type of message as 'DISCOVERY'
        message = Message(ownConnector, messageType, data)  # Creates the message object
        encodedMessage = BlockchainUtils.encode(message)  # Encodes the message using BlockchainUtils
        return encodedMessage  # Returns the encoded handshake message

    def handleMessage(self, message):
        """
        Handles a message received from another peer node.

        This method processes a discovery message from another node, checks if any new peers are included
        in the message, and attempts to connect to any peers that are not already known.

        :param message: The received message containing information about peers.
        """
        peersSocketConnector = message.senderConnector  # Gets the connector of the sender node
        peersPeerList = message.data  # Gets the list of peers from the sender node
        newPeer = True  # Flag to track if the peer is new

        # Checks if the sender node is already known (i.e., already in the peer list)
        for peer in self.socketCommunication.peers:
            if peer.equals(peersSocketConnector):
                newPeer = False  # The peer is already in the list

        if newPeer:
            self.socketCommunication.peers.append(peersSocketConnector)  # Adds the new peer to the peer list

        # Attempts to connect to any new peers that were provided in the message
        for peersPeer in peersPeerList:
            peerKnown = False
            for peer in self.socketCommunication.peers:
                if peer.equals(peersPeer):
                    peerKnown = True  # The peer is already known
            if not peerKnown and not peersPeer.equals(self.socketCommunication.socketConnector):
                # If the peer is not known and is not the local node itself, attempt to connect
                self.socketCommunication.connect_with_node(peersPeer.ip, peersPeer.port)  # Connect to the new peer
