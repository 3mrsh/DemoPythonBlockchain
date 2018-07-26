''' 
This is the file that will hold the instantiation of our classes & the logic for the demo.
'''
from blockchain import Node

#------------------
# Configure & create 

inlCBVal=15

nodePoE = Node(CBVal = inlCBVal)
blockchainPoE = nodePoE.blockchain
blockchainPoE.nodes.append(nodePoE)

nodeA = blockchainPoE.newNode()
nodeB = blockchainPoE.newNode()
nodeC = blockchainPoE.newNode()

#------------------
# Gen. some in'l currency by mining empty blocks.
nodeA.mine()
nodeA.mine()
nodeA.mine()
nodeA.mine()

nodeB.mine()
nodeB.mine()
nodeB.mine()

nodeC.mine()
nodeC.mine()

#------------------
# Send some transactions.








# nodeA.wallet.makeTransaction(nodeB.wallet.address, 100)


