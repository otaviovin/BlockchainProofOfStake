from BlockchainUtils import BlockchainUtils

class Lot():

    def __init__(self, publicKey, interation, lastBlockHash):
        self.publicKey = str(publicKey)
        self.interation = interation
        self.lastBlockHash = lastBlockHash

    def lotHash(self):
        hashData = self.publicKey + self.lastBlockHash
        for _ in range(self.interation):
            hashData = BlockchainUtils.hash(hashData).hexdigest()
        return hashData