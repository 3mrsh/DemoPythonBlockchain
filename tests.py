from blockchain import *
import itertools

inlCBVal=15

nodePoE = Node(CBVal = inlCBVal)
blockchainPoE = nodePoE.blockchain
blockchainPoE.nodes.append(nodePoE) #This introduces our nodePoE into the Blockchain.

nodeA = blockchainPoE.newNode()
nodeB = blockchainPoE.newNode()
nodeC = blockchainPoE.newNode()

''' All nodes have different, yet equivalent, instances of the Blockchain'''
print not(nodeA.blockchain.chain == nodeB.blockchain.chain) #Return True.
print vars(nodeA.blockchain.chain[0]) == vars(nodeB.blockchain.chain[0]) #Return True.

''' All nodes have copies of their fellow nodes'''
print nodeA.blockchain.nodes == nodeB.blockchain.nodes  #True
print nodePoE.blockchain.nodes[0] == nodePoE #True
print nodeA.blockchain.nodes[1] == nodeA #True
print nodeB.blockchain.nodes[2] == nodeB #True
print nodeB.blockchain.nodes[3] == nodeC #True
print( (len(nodePoE.blockchain.nodes) == len(nodeA.blockchain.nodes)) and 
    ((len(nodeA.blockchain.nodes) == len(nodeB.blockchain.nodes))) and 
    ((len(nodeB.blockchain.nodes) == len(nodeC.blockchain.nodes)))
) #True

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

''' All nodes have the same # of blocks. '''
# print( (len(nodePoE.blockchain.chain) == len(nodeA.blockchain.chain)) and 
#     ((len(nodeA.blockchain.chain) == len(nodeB.blockchain.chain))) and 
#     ((len(nodeB.blockchain.chain) == len(nodeC.blockchain.chain)))
# ) #True
# for a,b in list(itertools.combinations([nodePoE, nodeA, nodeB, nodeC],2)):
#     for c,d in zip(a.blockchain.chain,b.blockchain.chain):
#         if c==d:
#             print 'c==d' #Never print
#         if vars(c)!=vars(d):
#             print "vars(c)!=vars(d)" #Never print


#------------------
# Send some transactions.
#To run tests; check:
#nodeA.wallet.getUTXOs(getAll=True)[1]
#nodeA.wallet.getIncompleteUTXOInfo(getAll=True)[1]

nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10)
len(nodeA.blockchain.incompl_transxns)
len(nodeB.blockchain.incompl_transxns)
len(nodeC.blockchain.incompl_transxns)
len(nodePoE.blockchain.incompl_transxns)
len(nodeA.blockchain.my_incompl_transxns)
len(nodeB.blockchain.my_incompl_transxns)
len(nodeC.blockchain.my_incompl_transxns)


nodeB.mine()
nodeB.wallet.makeTransaction(rcpt_address=nodeC.wallet.address, val = 90)
len(nodeA.blockchain.incompl_transxns)
len(nodeB.blockchain.incompl_transxns)
len(nodeC.blockchain.incompl_transxns)
len(nodeA.blockchain.my_incompl_transxns)
len(nodeB.blockchain.my_incompl_transxns)
len(nodeC.blockchain.my_incompl_transxns)


nodeC.mine()
len(nodeA.blockchain.incompl_transxns)
len(nodeB.blockchain.incompl_transxns)
len(nodeC.blockchain.incompl_transxns)
len(nodeA.blockchain.my_incompl_transxns)
len(nodeB.blockchain.my_incompl_transxns)
len(nodeC.blockchain.my_incompl_transxns)

nodeC.wallet.makeTransaction(rcpt_address = nodeB.wallet.address, val = 135)
nodeC.wallet.makeTransaction(rcpt_address = nodeB.wallet.address, val = 1)
nodeA.mine()


