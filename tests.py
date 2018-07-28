# execfile('tests.py')
''' 
This is the file that will hold the instantiation of our classes & the logic for the demo.
'''

from blockchain import *
import itertools

inlCBVal=15

def newTestingEnv():
    #Config
    nodePoE = Node(CBVal = inlCBVal)
    blockchainPoE = nodePoE.blockchain
    blockchainPoE.nodes.append(nodePoE)
    nodeA = blockchainPoE.newNode()
    nodeB = blockchainPoE.newNode()
    nodeC = blockchainPoE.newNode()
    nodeA.mine(_print=False)
    nodeA.mine(_print=False)
    nodeA.mine(_print=False)
    nodeA.mine(_print=False)
    nodeB.mine(_print=False)
    nodeB.mine(_print=False)
    nodeB.mine(_print=False)
    nodeC.mine(_print=False)
    nodeC.mine(_print=False)
    return (nodeA, nodeB, nodeC)

def test1():
    (nodeA, nodeB, nodeC) = newTestingEnv()
    num_txns = 1
    print 'nodeA initial balance==60?', nodeA.wallet.getBalance() == 60

    for i in range(1,num_txns+1):
        trans1 = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10, _print=False)
        print 'After ', str(i), ' pending txn, nodeA balance == (60-', str(10*i),'?', nodeA.wallet.getBalance() == (60-10)

    print 'After ', str(num_txns),' pending txn, nodeB balance == 45?', nodeB.wallet.getBalance() == 45
    nodeB.mine()
    print 'After all of its txn is mined, nodeA balance ==', (60-num_txns*10),'?', nodeA.wallet.getBalance() == (60 - num_txns*10)
    print 'After mining a block with all the txns, nodeB balance == (45+15+', str(num_txns*10),')?', nodeB.wallet.getBalance() == (45+15+num_txns*10)
    print 'If all printed booleans are True, the test was succesful.'

def test2():
    (nodeA, nodeB, nodeC) = newTestingEnv()
    num_txns = 2
    print 'nodeA initial balance==60?', nodeA.wallet.getBalance() == 60

    for i in range(1,num_txns+1):
        trans = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10, _print=False)
        print 'After ',str(i),' pending txns, nodeA balance == (60-',str(10*i),')?', nodeA.wallet.getBalance() == (60-10*i)

    print 'After ', str(num_txns),' pending txn, nodeB balance == 45?', nodeB.wallet.getBalance() == 45
    nodeB.mine()
    print 'After all of its txn is mined, nodeA balance == ', (60-num_txns*10) ,'?', nodeA.wallet.getBalance() == (60 - num_txns*10)
    print 'After mining a block with all the txns, nodeB balance == (45+15+', str(num_txns*10),')?', nodeB.wallet.getBalance() == (45+15+num_txns*10)
    print 'If all printed booleans are True, the test was succesful.'

def test3():
    (nodeA, nodeB, nodeC) = newTestingEnv()
    num_txns = 3
    print 'nodeA initial balance==60?', nodeA.wallet.getBalance() == 60

    for i in range(1,num_txns+1):
        trans = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10, _print=False)
        print 'After ',str(i),' pending txns, nodeA balance == (60-',str(10*i),')?', nodeA.wallet.getBalance() == (60-10*i)
    
    print 'After ', str(num_txns),' pending txn, nodeB balance == 45?', nodeB.wallet.getBalance() == 45
    nodeB.mine()
    print 'After all of its txn is mined, nodeA balance ==', (60-num_txns*10),'?', nodeA.wallet.getBalance() == (60 - num_txns*10)
    print 'After mining a block with all the txns, nodeB balance == (45+15+', str(num_txns*10),')?', nodeB.wallet.getBalance() == (45+15+num_txns*10)
    print 'If all printed booleans are True, the test was succesful.'

def test4():
    (nodeA, nodeB, nodeC) = newTestingEnv()
    num_txns = 4
    print 'nodeA initial balance==60?', nodeA.wallet.getBalance() == 60

    for i in range(1,num_txns+1):
        trans = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10, _print=False)
        print 'After ',str(i),' pending txns, nodeA balance == (60-',str(i*10),')?', nodeA.wallet.getBalance() == (60-10*i)
    
    print 'After ', str(num_txns),' pending txn, nodeB balance == 45?', nodeB.wallet.getBalance() == 45
    nodeB.mine()
    print 'After all of its txn is mined, nodeA balance ==', (60-num_txns*10),'?', nodeA.wallet.getBalance() == (60 - num_txns*10)
    print 'After mining a block with all the txns, nodeB balance == (45+15+', str(num_txns*10),')?', nodeB.wallet.getBalance() == (45+15+num_txns*10)
    print 'If all printed booleans are True, the test was succesful.'

def test5(): 
    (nodeA, nodeB, nodeC) = newTestingEnv()
    num_txns = 5 
    print 'nodeA initial balance==60?', nodeA.wallet.getBalance() == 60

    for i in range(1,num_txns+1):
        trans = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10, _print=False)
        print 'After ',str(i),' pending txns, nodeA balance == (60-',str(i*10),')?', nodeA.wallet.getBalance() == (60-10*i)

    print 'After ', str(num_txns),' pending txn, nodeB balance == 45?', nodeB.wallet.getBalance() == 45
    nodeB.mine()
    print 'After 4 of its 5 txns are mined, nodeA balance ==', (60-num_txns*10),'?', nodeA.wallet.getBalance() == (60 - num_txns*10)
    print 'After mining a block with 4 of nodeAs 5 txns, nodeB balance == (45+15+', str(4*10),')?', nodeB.wallet.getBalance() == (45+15+4*10)
    print 'This is because a block can only hold 5 txns, with the 1st reserved for the Coinbase transaction'
    print 'Confirm that there are still incomplete_transactions? ', (len(nodeB.blockchain.incompl_transxns)==len(nodeC.blockchain.incompl_transxns)) and (len(nodeB.blockchain.incompl_transxns)>0)
    print 'Now if anyone mines a new block with the pending transxns (here we select C to do so)'
    nodeC.mine()
    print 'After all of its txns are mined, nodeA balance ==', (60-num_txns*10),'?', nodeA.wallet.getBalance() == (60-num_txns*10)
    print 'After receiving all of the txns & mining 1 addl block, nodeB balance == (45+15+50)?', nodeB.wallet.getBalance() == (45+15+num_txns*10)
    print 'After mining an addl block, nodeCs balance == 45?', nodeC.wallet.getBalance() == (30+15)
    print 'If all printed booleans are True, the test was succesful.'
    
#Problem: nodeB.wallet.getBalance()==10
def test6():
    (nodeA, nodeB, nodeC) = newTestingEnv()
    num_txns = 6
    print 'nodeA initial balance==60?', nodeA.wallet.getBalance() == 60

    for i in range(1,num_txns+1):
        trans = nodeA.wallet.makeTransaction(rcpt_address=nodeB.wallet.address, val=10, _print=False)
        print 'After ',str(i),' pending txns, nodeA balance == (60-',str(i*10),')?', nodeA.wallet.getBalance() == (60-10*i)

    print 'After ', str(num_txns),' pending txn, nodeB balance == 45?', nodeB.wallet.getBalance() == 45
    nodeB.mine()
    print 'After 4 of its 6 txns are mined, nodeA balance ==', (60-num_txns*10),'?', nodeA.wallet.getBalance() == (60 - num_txns*10)
    print 'After mining a block with 4 of nodeAs 6 txns, nodeB balance == (45+15+', str(4*10),')?', nodeB.wallet.getBalance() == (45+15+4*10)
    print 'This is because a block can only hold 6 txns, with the 1st reserved for the Coinbase transaction'
    print 'Confirm that there are still incomplete_transactions? ', (len(nodeB.blockchain.incompl_transxns)==len(nodeC.blockchain.incompl_transxns)) and (len(nodeB.blockchain.incompl_transxns)>0)
    print 'Now if anyone mines a new block with the pending transxns (here we select C to do so)'
    nodeC.mine()
    print 'After all of its txns are mined, nodeA balance ==', (60-num_txns*10),'?', nodeA.wallet.getBalance() == (60-num_txns*10)
    print 'After receiving all of the txns & mining 1 addl block, nodeB balance == (45+15+60)?', nodeB.wallet.getBalance() == (45+15+num_txns*10)
    print 'After mining an addl block, nodeCs balance == 45?', nodeC.wallet.getBalance() == (30+15)
    print 'If all printed booleans are True, the test was succesful.'