# Dependencies:
    PyCryptodome (https://pycryptodome.readthedocs.io/en/latest/src/introduction.html)
    base58: (https://pypi.org/project/base58/)

# Overview:

The idea in this project is to implement a simple Blockchain P.o.C. in Python.
It will be run in the terminal, as opposed to put on a server. The multiple nodes will therefore all be part of a single terminal.
We will try to use asyncronous operations to be able to send & receive transactions to nodes that are busy mining, and also to send 
& receive blocks among nodes.

# Notation:
We will refer to all transactions that have been undertaken but have yet to be included in a Block in the Blockchain as 'incomplete transactions'.

# Architecture:
For the demo, there will be 4 nodes, each representing one individual connected to OmarsBlockchain. These nodes will be named NodeA-NodeD.
In the spirit of decentralization, each node will have their own copy of the Blockchain. They will also have keys & an address to identify 
& interact with each other.  
Nodes will be able to Mine & Initiate transactions. 
Nodes will mine by looking at their copy of the Blockchain to see the previous-hash, and the list of uncompleted transactions. It will then
generate and store a Merkle Tree from this set of uncompleted transactions. With this done, it will attempt to satisfy the Proof of Work,
changing the nonce and hashing the updated header (nonce, merkle tree, prev. header) repeatedly until it starts with the correct # of 0s.

While it would make sense to add these methods to the Blockchain class, it may make more sense to include them in the Node class as it will be the node who performs them. 

Note the usage of passing-by-reference and passing-by-value ([:]) when we instantiate a Node and its wallet. Each node gets a copy of the PoEnode
    
Each blockchain member will be a separate instance of 
the class Blockchain defined in our code. The Blockchain class has a set of Nodes, 
Blocks, & Incomplete Transactions.

07/26:  The current VerifyTransactions feature is called whenever a Transaction is broadcast to all Nodes, which occurs whenever a regular (non-Coinbase) transaction is made. Since Coinbase Txns are never broadcast individually, and are only shared when the Blocks they are embedded in are shared, we will handle their verification as part of the Block verification. At least that is the plan for now.

# Limitations & Next Steps:
Unfortunately at this stage, it seems too difficult to implement the asyncronous communication needed between the different nodes here. 
Python runs only on a single-thread, and therefore it seems unlikely that (1) >1 node can mine at a same time; (2) any other node can have any other action while 1 node is mining; (3) nodes which are mining will be able to receive & interpret new transactions/blocks.
Therefore, we may have it that only 1 node can run any action at a time: this amounts to a full-lock on other actions while any action is running. But maybe we can solve that..

We haven't implemented a function to generate >1 address for public key; therefore, our Wallet (as defined by a private key uniquely determining a public key) can only expose 1 address. This is reflected in our nomenclature: we use address rather than addresses

"Block size" has not been implemented; instead, nodes are told how many transactions can fit in a node arbitrarily.

We haven't implemented nor attempted to use the Blockchain Script language. As a result, our creation and verification of transactions is very different. When nodes attempt to verify the scripts in a transaction, they simply look at the 'verified' member of a Transaction. Therefore, their verification is simply checking that an earlier test was passed, rather than doing any tests of their own. While an obvious shortcoming, this is a fair first step and works in our modest demo purpose.

We haven't implemented Transaction Fees; a miner only receives the CB amount. In that vain, there is also only an arbitrary method for selecting pending transactions to include in a block.

We currently 'subtract' someone's funds immediately; whereas in reality, a UTXO is not 'used' until the transaction is in a block, added to the Blockchain. If we want to implement that stall, we need to also ensure we either avoid selecting the same UTXOs (as then the transactions would be cancelled) or co-ordinate them so one uses the 'change' of the other.

We have made the conscious decision to allow each Node to store (in its instance of the blockchain's nodes class), a Reference to each of its fellow nodes. That means that the singleton instance of each node can be accessed by each other node. The alternative would have been to pass in a copy of each Node, thereby preventing nodes from interfering with each other and more accurately capturing the Blockchain security protocls. But, given the large memory footprint that would be needed to copy each Node (and with that, their copies of the Blockchain  [which may well result in an infinite loop] ), we decide against that. A future iteration could build this chain with a simplified NeighborNode class that merely holds the address of each nodes, and, somehow, the ability to access the Nodes via the NotifyNodes() method on them only. For this demo, we just assume users would not call malicious functions.


# Resources:
    Encryption implemented acc. to : https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses
    Merkle Tree behavior:
    https://bitcoin.stackexchange.com/questions/77222/how-would-you-find-the-merkle-root-with-a-block-that-contains-6-transactions

# Merkle Trees:
    The height (from hashed transactions to root) is ceil(log_2(#T))
    Height then determines # of leaf nodes needed: 2^height
    If we have even #, we extend the last 2 to fill out empty spaces.
    If we have odd #, we extend the last 1 to fill out empty spaces.

# Questions (to be iterated thru as I build this):
Should each node get the same transaction? Or only a copy of it? Let's come back to this later.
