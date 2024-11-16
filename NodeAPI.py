from flask_classful import FlaskView, route
from flask import Flask, jsonify, request
from BlockchainUtils import BlockchainUtils

node = None  # Global variable to store the node instance


class NodeAPI(FlaskView):
    # Class to manage the Node's API

    def __init__(self):
        self.app = Flask(__name__)  # Initializes the Flask application

    def start(self, port):
        """
        Registers the routes and starts the Flask application.

        :param port: Port number for the Flask application
        """
        NodeAPI.register(self.app, route_base='/')  # Registers the class as a controller
        self.app.run(host='localhost', port=port)  # Starts the Flask server

    def injectNode(self, injectedNode):
        """
        Injects the node instance into the class.

        :param injectedNode: The node instance to be injected
        """
        global node  # Uses the global node variable
        node = injectedNode  # Stores the node instance

    @route('/info', methods=['GET'])
    def info(self):
        """
        Route to get information about the API.

        :return: Information about the communication interface to the node's blockchain
        """
        return 'This is a communication interface to a node\'s blockchain', 200

    @route('/blockchain', methods=['GET'])
    def blockchain(self):
        """
        Route to get the JSON representation of the blockchain.

        :return: The blockchain in JSON format
        """
        return node.blockchain.toJson(), 200

    @route('/transactionPool', methods=['GET'])
    def transactionPool(self):
        """
        Route to get the transaction pool.

        :return: A JSON object with the transactions in the pool
        """
        transactions = {}
        for ctr, transaction in enumerate(node.transactionPool.transactions):
            transactions[ctr] = transaction.toJson()  # Adds each transaction to the dictionary
        return jsonify(transactions), 200  # Returns the transactions as JSON

    @route('/transaction', methods=['POST'])
    def transaction(self):
        """
        Route to receive a new transaction.

        :return: A response indicating the result of processing the transaction
        """
        values = request.get_json()  # Gets the JSON data from the request
        if not 'transaction' in values:
            return 'Missing transaction value', 400  # Returns an error if no transaction is provided
        transaction = BlockchainUtils.decode(values['transaction'])  # Decodes the transaction
        node.handleTransaction(transaction)  # Processes the transaction in the node
        response = {'message': 'Received transaction'}  # Success response
        return jsonify(response), 201  # Returns the success message as JSON
