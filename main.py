from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
from Node import Node
import sys
import pprint

if __name__ == '__main__':

  print("Iniciando o script...")

  ip = sys.argv[1]
  port = int(sys.argv[2])

  node = Node(ip, port)
  node.startP2P()

  