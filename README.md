# BlockchainProofOfStake

Transactions to Proof of Stake Consensus in own P2P Network of Nodes in Python. Decentralized P2P Network. Finding Consensus in a Network of mutually untrusted Nodes. REST-API to communicate with your own Blockchain

Working with:
Cryptographic Signatures
RSA Public Key Cryptography
SHA-256 Hashes
Transactions - The purpose of Transactions in a Blockchain Systems.
Blocks - The most essential building block.
Blockchains - Whats going on behind the scenes.
P2P Network - How to find and communicate with other Nodes.
REST API - How to make use of your Blockchain System.
P2P Peer Discovery
Socket Communication
REST Endpoints
Threading & Parallelization

## Test commands

### cmd:

python main.py localhost 10001 5000 keys/genesisPrivateKey.pem
python main.py localhost 10002 5001 
python main.py localhost 10003 5003 keys/stakerPrivateKey.pem
python Interaction.py

### browser:

localhost:5000/blockchain
localhost:5001/blockchain
localhost:5003/blockchain

