class Message():
    def __init__(self, senderConnector, messageType, data):
        """
        Initializes the Message class with the following attributes:
        
        :param senderConnector: The connector that sent the message
        :param messageType: The type of the message (e.g., 'TRANSACTION', 'BLOCK', etc.)
        :param data: The data contained in the message, which may include relevant information
        """
        self.senderConnector = senderConnector  # Stores the sender's connector
        self.messageType = messageType          # Stores the type of the message
        self.data = data                        # Stores the message data
