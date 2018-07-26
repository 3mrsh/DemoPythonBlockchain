#This is just a To-do list:

1) Implement Coin-base Transaction.
I think the idea is to create this transaction immediately when you start mining. It apparently should be included as the First (Leftmost) transaction of the Merkle Tree.
Generating a Coin-base Transaction requires only the miner's address. We can easily put this into a function in the Blockchain member. Unlike any other transaction, we won't broadcast this to other nodes. Unlike the other transactions, this transaction should not be executed if the individual node does not succesfuly finish mining his block.
This should be in the same space we generate our Merkle Tree. Therefore, in the Block!

2) Implement Proof of Work

3) Build out Validation on the part of non-Miner nodes.

4) Change not'n from 'incomplete transactions' to 'pending transactions'.

#Optional Next Steps:
1) Improve Merkle Tree function by cutting out the re-calculation of the same hashes in event of repetition. Ex: [1,2,3,4,5] calculates hash(5,5) 2x.

Wouldn't a way to do that, just feasibly be to create an array in the formatMerkleTree function that is range(len(transactions)), and update that so we get something more easy to work with.
And then store in memory which pairs have already been calculated?
This prevents longer & more complicated calculations with long addresses and transaction ids.

2) Set up a BlockHeader & BlockBody class to better represent Architecture of a block.
BlockHeader: Previous Hash, Merkle Root, Nonce. 
BlockBody: simply the list of Transactions.
