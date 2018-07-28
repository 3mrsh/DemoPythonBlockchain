# execfile('script.py')
''' 
This is the file that will hold the instantiation of our classes & the logic for the demo.
'''

from blockchain import *
import itertools

###############################################
## Network Configuration: 
#
###############################################
#Initial coin base value
inlCBVal=15

#Create Point-of-Entry Node, dedicated to introducing new nodes to the Network.
nodePoE = Node(CBVal = inlCBVal)
blockchainPoE = nodePoE.blockchain
blockchainPoE.nodes.append(nodePoE)



###############################################
## Populate Network with Nodes: 
#
###############################################
nodeA = blockchainPoE.newNode()
nodeB = blockchainPoE.newNode()
nodeC = blockchainPoE.newNode()
nodeD = blockchainPoE.newNode()


###############################################
## Introduce Initial Currency by Mining Empty 
# Blocks:
###############################################
nodeA.mine()
nodeA.mine()
nodeA.mine()
nodeA.mine()

nodeB.mine()
nodeB.mine()
nodeB.mine()

nodeC.mine()
nodeC.mine()

nodeD.mine()

###############################################
## Begin Normal Market Operations :
# Transactions & Mining, double-spending, over-spending
#  and different types of transactions mixed in.
# 
###############################################

nodeA.wallet.makeTransaction(nodeB.wallet.address, 30)
nodeA.wallet.makeTransaction(nodeB.wallet.address, 20)
nodeB.wallet.makeTransaction(nodeA.wallet.address, 15)
nodeB.wallet.makeTransaction(nodeC.wallet.address, 15)
nodeD.mine()
nodeD.wallet.makeTransaction(nodeA.wallet.address, 20)
nodeB.wallet.makeTransaction(nodeA.wallet.address, 20)
nodeC.wallet.makeTransaction(nodeA.wallet.address, 20)
nodeD.mine()
nodeC.mine()
nodeC.mine()
nodeC.wallet.makeTransaction(nodeB.wallet.address,15)
nodeC.wallet.makeTransaction(nodeB.wallet.address,50)
nodeC.wallet.makeTransaction(nodeB.wallet.address,40)