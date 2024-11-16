class SocketConnector():
    # Class that represents a socket connection, identifying a node by its IP and port.

    def __init__(self, ip, port):
        """
        Initializes a socket connector with the specified IP and port.
        
        :param ip: The IP address of the node.
        :param port: The port number used for communication.
        """
        self.ip = ip  # Assigns the IP address to the connector
        self.port = port  # Assigns the port number to the connector

    def equals(self, connector):
        """
        Compares this socket connector with another to check if they are equal based on IP and port.

        :param connector: The other SocketConnector instance to compare with.
        :return: True if both the IP address and port are equal, False otherwise.
        """
        if connector.ip == self.ip and connector.port == self.port:
            return True  # Returns True if the connectors are identical
        else:
            return False  # Returns False if the connectors are different
