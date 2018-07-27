''' 
This is the file that will hold the instantiation of our classes & the logic for the demo.
'''

from blockchain import Node
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



###############################################
## Introduce Initial Currency by Mining: 
#
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



###############################################
## Begin Normal Market Operations :
# Transactions & Mining, double-spending, over-spending
#  and different types of transactions mixed in.
# 
###############################################
a = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
nodeA.wallet.getBalance()
a = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
nodeA.wallet.getBalance()
a = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
nodeA.wallet.getBalance()
a = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
nodeA.wallet.getBalance()
a = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
nodeA.wallet.getBalance()
a = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
nodeA.wallet.getBalance()
a = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=1)
nodeA.wallet.getBalance()
nodeB.wallet.getBalance()
nodeC.wallet.getBalance()

nodeB.mine()
nodeA.wallet.getBalance()
nodeB.wallet.getBalance() 
nodeC.wallet.getBalance()
nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)

nodeB.wallet.makeTransaction(rcpt_address=nodeC.wallet.address, val = 90)

nodeC.mine()

nodeC.wallet.makeTransaction(rcpt_address = nodeB.wallet.address, val = 135)
nodeC.wallet.makeTransaction(rcpt_address = nodeB.wallet.address, val = 1)

nodeA.mine()


