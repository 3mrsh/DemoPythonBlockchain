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



###############################################
## Begin Normal Market Operations :
# Transactions & Mining, double-spending, over-spending
#  and different types of transactions mixed in.
# 
###############################################
def test1():
    print 'A=', nodeA.wallet.getBalance() == 60
    trans1 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == (60-10)
    print 'B=', nodeB.wallet.getBalance() == 45
    nodeB.mine()
    print 'C=', nodeA.wallet.getBalance() == (60-10)
    print 'D=', nodeB.wallet.getBalance() == (45+15+10)

def test2():
    print 'A=', nodeA.wallet.getBalance() == 60
    trans1 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == (60-10)
    trans2 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == (60-20)
    print 'B=', nodeB.wallet.getBalance() == 45
    nodeB.mine()
    print 'C=', nodeA.wallet.getBalance() == (60-20)
    print 'D=', nodeB.wallet.getBalance() == (45+15+20)

def test3():
    print 'A=', nodeA.wallet.getBalance() == 60
    trans1 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == 50
    trans2 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == 40
    trans3 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == 30
    print 'B=', nodeB.wallet.getBalance() == 45
    nodeB.mine()
    print 'C=', nodeA.wallet.getBalance() == (60-30)
    print 'D=', nodeB.wallet.getBalance() == (45+15+30)

def test4():
    print 'A=', nodeA.wallet.getBalance() == 60
    trans1 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == (60-10)
    trans2 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == (60-20)
    trans3 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == (60-30)
    trans4 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == (60-40)
    print 'B=', nodeB.wallet.getBalance() == 45
    nodeB.mine()
    print 'C=', nodeA.wallet.getBalance() == (60-40)
    print 'D=', nodeB.wallet.getBalance() == (45+15+40)

def test5(): 
    print 'A=', nodeA.wallet.getBalance() == 60
    trans1 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == (60-10)
    trans2 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == (60-20)
    trans3 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == (60-30)
    trans4 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == (60-40)
    trans5 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == (60-50)
    print 'B=', nodeB.wallet.getBalance() == 45
    nodeB.mine()
    print 'C=', nodeA.wallet.getBalance() == (60-50)
    print 'D=', nodeB.wallet.getBalance() == (45+15+40)
    print '(failed?) D= ', nodeB.wallet.getBalance() == 100
    print 'But, now if someone else mines a block w/ the pending transxns'
    print 'E=', (len(nodeB.blockchain.incompl_transxns)==len(nodeC.blockchain.incompl_transxns)) and (len(nodeB.blockchain.incompl_transxns)>0)
    nodeC.mine()
    print 'F=', nodeA.wallet.getBalance() == (60-50)
    print 'G=', nodeB.wallet.getBalance() == (45+15+50)
    print 'H=', nodeC.wallet.getBalance() == (30+15)
    
#Problem: nodeB.wallet.getBalance()==10
def test6():
    print 'A=', nodeA.wallet.getBalance() == 60
    trans1 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == (60-10)
    trans2 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == (60-20)
    trans3 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == (60-30)
    trans4 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == (60-40)
    trans5 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == (60-50)
    trans6 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
    print 'A=', nodeA.wallet.getBalance() == (60-60)
    print 'B=', nodeB.wallet.getBalance() == 45
    nodeB.mine()
    print 'C=', nodeA.wallet.getBalance() == (60-60)
    print 'D=', nodeB.wallet.getBalance() == (45+15+40)
    print 'E=', (len(nodeB.blockchain.incompl_transxns)==len(nodeC.blockchain.incompl_transxns)) and (len(nodeB.blockchain.incompl_transxns)>0)
    nodeC.mine()
    print 'F=', nodeA.wallet.getBalance() == (60-60)
    print 'G=', nodeB.wallet.getBalance() == (45+15+60)
    print 'H=', nodeC.wallet.getBalance() == (30+15)

