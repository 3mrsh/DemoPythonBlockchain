# Dependencies:
PyCryptodome (https://pycryptodome.readthedocs.io/en/latest/src/introduction.html)
base58: (https://pypi.org/project/base58/)

# Overview:

The idea in this project is to implement a simple Blockchain P.o.C. in Python.
It will be run in the terminal, as opposed to put on a server. The multiple nodes will therefore all be part of a single terminal. 
In light of this, this project maintains only a somewhat Decentralized Infrastructure as will be expanded on later; each node has its own equivalent (yet separate)instance of the Blockchain, yet, for memory purposes, stores the same exact copy of a transaction. 
Analyzing the code may help one understand some of the moving parts of the Blockchain infrastructure.

# Notation:
We will refer to all transactions that have been undertaken but have yet to be included in a Block in a Blockchain as 'incomplete transactions' or 'pending transactions'.

# Architecture:
For the demo, there will be 4 nodes, each representing one individual connected to OmarsBlockchain. These nodes will be named NodeA-NodeD.
In the spirit of decentralization, each node will have their own copy of the Blockchain. They will also have keys & an address to be ID'd 
& interact with each other.

Nodes will be able to Initiate Transactions & Mine Blocks. Once done, they broadcast the new data-point to the other nodes connected to the BC, who independently verify it and either append it to their data or ignore it. 

Transactions are built-out as closely as possible to Bitcoin and other cryptocurrency's versions. Full-details can be found in the code.

Nodes will mine by looking at their instance of the Blockchain to see the previous-hash, and the list of uncompleted transactions. It will then
create a Block instance, get a Coinbase transaction, and then generate and store a Merkle Tree. With this done, it will attempt to satisfy the Proof of Work,
changing the nonce and hashing the updated header (nonce, merkle tree, prev. header) repeatedly until it starts with the correct # of 0s.

In the spirit of how Satoshi devised his Blockchain with Bitcoin in mind, each of our Nodes has a Wallet.

Each blockchain member will be a separate instance of the class Blockchain defined in our code. The Blockchain class has a set of Nodes, Blocks, & Incomplete Transactions.

As discussed in the next section, only 1 node can perform an action at a given time.

# Limitations & Next Steps:
Unfortunately at this stage, it seems too difficult to implement the asyncronous communication needed between the different nodes here. 
It would be too much of an endeavor to ensure that (1) >1 node can mine at a same time; (2) any other node can have any other action while 1 node is mining; (3) nodes which are mining will be able to receive & interpret new transactions/blocks.
Therefore, we may have it that only 1 node can run any action at a time: this amounts to a full-lock on other actions while any action is running. But maybe we can solve that..

We haven't implemented a function to generate >1 address for public key; therefore, our Wallet (as defined by a private key uniquely determining a public key) can only expose 1 address. This is reflected in our nomenclature: we use address rather than addresses

"Block size" has not been implemented; instead, nodes are told how many transactions can fit in a node arbitrarily.

We haven't implemented nor attempted to use the Blockchain Script language. As a result, our creation and verification of transactions is very different. When nodes attempt to verify the scripts in a transaction, they simply look at the 'verified' member of a Transaction. Therefore, their verification is simply checking that an earlier test was passed, rather than doing any tests of their own. While an obvious shortcoming, this is a fair first step and works in our modest demo purpose.

We haven't implemented Transaction Fees; a miner only receives the CB amount. In that vain, there is also only an arbitrary method for selecting pending transactions to include in a block.

We have made the conscious decision to allow each Node to store (in its instance of the blockchain's nodes class), a Reference to each of its fellow nodes. That means that the singleton instance of each node can be accessed by each other node. The alternative would have been to pass in a copy of each Node, thereby preventing nodes from interfering with each other and more accurately capturing the Blockchain security protocls. But, given the large memory footprint that would be needed to copy each Node (and with that, their copies of the Blockchain  [which may well result in an infinite loop] ), we decide against that. A future iteration could build this chain with a simplified NeighborNode class that merely holds the address of each nodes, and, somehow, the ability to access the Nodes via the NotifyNodes() method on them only. For this demo, we just assume users would not call malicious functions.


# Resources:
Encryption implemented acc. to : https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses
Merkle Tree behavior: https://bitcoin.stackexchange.com/questions/77222/how-would-you-find-the-merkle-root-with-a-block-that-contains-6-transactions

# Further Notes:
The current VerifyTransactions feature is called whenever a Transaction is broadcast to all Nodes, which occurs whenever a regular (non-Coinbase) transaction is made. Since Coinbase Txns are never broadcast individually, and are only shared when the Blocks they are embedded in are shared, we will handle their verification as part of the Block verification. At least that is the plan for now.

