from BlockchainUtils import BlockchainUtils
from Lot import Lot


class ProofOfStake():
    # Class responsible for the Proof of Stake (PoS) logic in the blockchain

    def __init__(self):
        """
        Initializes the ProofOfStake class and sets up the stakers dictionary.
        The genesis node's stake is also set during initialization.
        """
        self.stakers = {}  # A dictionary to store stakers (participants who perform staking)
        self.setGenesisNodeStake()  # Sets the stake for the genesis node

    def setGenesisNodeStake(self):
        """
        Sets the initial stake for the genesis node.
        Reads the public key of the genesis node from a file and assigns it a stake of 1.
        """
        genesisPublicKey = open('keys/genesisPublicKey.pem', 'r').read()  # Reads the public key of the genesis node from a file
        self.stakers[genesisPublicKey] = 1  # Assigns a stake of 1 to the genesis node

    def update(self, publicKeyString, stake):
        """
        Updates the stake of an existing participant or adds a new participant.
        
        :param publicKeyString: The public key of the participant.
        :param stake: The stake to be added or updated.
        """
        if publicKeyString in self.stakers.keys():
            self.stakers[publicKeyString] += stake  # Increases the stake if the participant is already in the stakers list
        else:
            self.stakers[publicKeyString] = stake  # Adds a new staker with the specified stake

    def get(self, publicKeyString):
        """
        Returns the stake of a participant, if they exist.

        :param publicKeyString: The public key of the participant.
        :return: The stake of the participant or None if the participant does not exist.
        """
        if publicKeyString in self.stakers.keys():
            return self.stakers[publicKeyString]  # Returns the stake if the participant is found
        else:
            return None  # Returns None if the participant does not exist

    def validatorLots(self, seed):
        """
        Generates a list of "lots" (tickets) for each validator based on their stake.

        :param seed: A seed used to generate unique identifiers for each "lot".
        :return: A list of "lots" corresponding to each validator's stake.
        """
        lots = []  # A list to store the lots (tickets)
        for validator in self.stakers.keys():
            for stake in range(self.get(validator)):  # Creates one "lot" for each unit of stake
                lots.append(Lot(validator, stake + 1, seed))  # Creates a new "lot" for each unit of stake
        return lots  # Returns the list of "lots"

    def winnerLot(self, lots, seed):
        """
        Determines the winning "lot" based on the smallest offset in relation to a reference hash.

        :param lots: The list of "lots" to evaluate.
        :param seed: The seed used to generate the reference hash.
        :return: The winning "lot" object.
        """
        winnerLot = None  # The winning lot, initially set to None
        leastOffset = None  # The least offset, initially set to None
        referenceHashIntValue = int(BlockchainUtils.hash(seed).hexdigest(), 16)  # Converts the reference hash into an integer

        for lot in lots:
            lotIntValue = int(lot.lotHash(), 16)  # Converts the lot's hash into an integer
            offset = abs(lotIntValue - referenceHashIntValue)  # Calculates the offset relative to the reference hash
            if leastOffset is None or offset < leastOffset:  # Checks if this lot has the smallest offset so far
                leastOffset = offset
                winnerLot = lot  # Updates the winning lot

        return winnerLot  # Returns the winning lot with the smallest offset

    def forger(self, lastBlockHash):
        """
        Selects the forger (validator) based on the hash of the last block.

        :param lastBlockHash: The hash of the last block, used to determine the winner.
        :return: The public key of the validator (forger) chosen to create the next block.
        """
        lots = self.validatorLots(lastBlockHash)  # Generates the "lots" for the validators based on the last block's hash
        winnerLot = self.winnerLot(lots, lastBlockHash)  # Determines the winning "lot" based on the reference hash
        return winnerLot.publicKey  # Returns the public key of the winning validator (forger)
