# execfile('tests.py')
from blockchain import Node, Blockchain, Block
import math, json

''' Set 1 '''
''' Adding a new Node should update all nodes' Blockchains '''
#Test addresses: All are correct.
inlCBVal = 15

NodePoE = Node(CBVal = inlCBVal)
BlockchainPoE = NodePoE.blockchain
NodePoE.blockchain.nodes.append(NodePoE)

nodeA = BlockchainPoE.newNode()
nodeB = BlockchainPoE.newNode()
nodeC = BlockchainPoE.newNode()

''' Set 2 '''
''' Mine a few blocks. '''
b1 = nodeA.mine()
b2 = nodeA.mine()
b3 = nodeA.mine()

b4 = nodeB.mine()
b5 = nodeB.mine()

b6 = nodeC.mine()

''' Set 3 ''' 
''' Now let's test. Each node should have a BC w/ 6  '''
