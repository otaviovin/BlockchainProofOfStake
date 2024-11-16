from BlockchainUtils import BlockchainUtils  # Importing utility functions for the blockchain

class Lot():
    def __init__(self, publicKey, iteration, lastBlockHash):
        """
        Initializes a new instance of Lot.

        :param publicKey: The public key associated with the lot
        :param iteration: The number of iterations to generate the hash
        :param lastBlockHash: The hash of the last block
        """
        self.publicKey = str(publicKey)  # Stores the public key as a string
        self.iteration = iteration  # Stores the number of iterations
        self.lastBlockHash = str(lastBlockHash)  # Stores the last block's hash as a string

    def lotHash(self):
        """
        Generates the hash for the lot by combining the public key and the last block's hash.

        The hash is generated iteratively, applying the hashing function a specified number of times.

        :return: The resulting hash of the lot
        """
        # Combine the public key and the last block's hash into a single string
        hashData = self.publicKey + self.lastBlockHash  
        # Perform the hashing operation for the specified number of iterations
        for _ in range(self.iteration):  
            # Generate the hash for the current data and update hashData
            hashData = BlockchainUtils.hash(hashData).hexdigest()  
        return hashData  # Return the final hash of the lot
