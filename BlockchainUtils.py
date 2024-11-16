from Crypto.Hash import SHA256  # Importing the SHA256 hashing algorithm
import json  # Module for JSON serialization and deserialization
import jsonpickle  # Library for serializing and deserializing Python objects

class BlockchainUtils():
    @staticmethod
    def hash(data):
        """
        Generates a SHA-256 hash for a given object.

        :param data: The object to be hashed
        :return: The generated hash object
        """
        dataString = json.dumps(data)  # Converts the object into a JSON string
        dataBytes = dataString.encode('utf-8')  # Encodes the string into bytes
        dataHash = SHA256.new(dataBytes)  # Creates a new SHA-256 hash from the bytes
        return dataHash  # Returns the hash object

    @staticmethod
    def encode(objectToEncode):
        """
        Encodes an object using jsonpickle.

        :param objectToEncode: The object to be encoded
        :return: The encoded representation of the object
        """
        return jsonpickle.encode(objectToEncode, unpicklable=True)  # Returns the encoded representation

    @staticmethod
    def decode(encodedObject):
        """
        Decodes an object that was encoded using jsonpickle.

        :param encodedObject: The encoded object to decode
        :return: The original object
        """
        return jsonpickle.decode(encodedObject)  # Returns the decoded object
