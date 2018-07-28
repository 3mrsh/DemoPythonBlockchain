# execfile("blockchain.py")

'''
This file will hold the foundational class logic for our Blockchain
'''

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, RIPEMD160
import base58, string, random, hashlib, time, json, math

class Blockchain:
    def __init__(self, nds=[], chain=[], inctrnsxns=[], CBval=None):
        ''' 
        Constructor.
        Note: nodes & transactions are stored as reference; chain is stored as copy.
        - nds (Node[]): A list of nodes connected to the BC
        - chain (Block[]): The list of blocks that comprise the chain
        - inctrnsxns (Transaction[]): A list of incomplete / pending transactions
        - CBval (number): Coinbase value; a.ka. payout for succesfully mining.
        '''
        self.nodes = nds[:] #: Node[]
        self.chain=[] #: Block[]
        self.incompl_transxns = inctrnsxns[:] #: Transaction[]
        self.my_incompl_transxns = [] #: Transaction[]; list of incompl_transactions.
        if chain:
            map(lambda x: self.newBlock(x), chain[:])
        else:
            self.chain = [ self.createGenesis() ] #: Block[]
        self.CBVal = CBval
    
    def createGenesis(self):
        '''
        Creates Genesis block. This fnx will be called only once: in the initialization of BlockchainPoE only.
        CBVal not added b/c this Block is not mined. Its just added to the Chain.
         Returns: Genesis Block
        '''
        return Block(n="this is the genesis block, therefore this text is arbitrary", isGenesis=True)

    def isValid(self, block):
        '''
        UNIMPLEMENTED

        Tests validity of (1) the block against hashes of previous blocks and (2) transactions within the block
        - block (Block): block to be tested
        Returns: boolean
        '''

        return True

    def notifyNodes(self, data=None, newNode=False, newBlock=False, newTransxn=False, newCBVal = False):
        '''
        Notifies each nodes in object's nodes member of 1 of 3 events.
        - data (Node | Block | Transaction | number): The elt to broadcast
        - newNode (boolean): New Node was added
        - newBlock (boolean): New Block was added
        - newTransxn (boolean): New Transaction was added
        - newCBVal (boolean): Whether Coinbase Val was changed.
        Returns: Nothing
        '''
        for node in self.nodes:
            node.updateInfo(data=data, newNode=newNode, newBlock=newBlock, newTransxn=newTransxn, newCBVal=newCBVal)
        return

    def newBlock(self, block):
        ''' 
        Add block to chain of this blockchain.
         - block (Block): block to be added
        Returns: Nothing
        '''
        # 1) Test validity of block's hash.
        validity = self.isValid(block)
        # 2) If valid: add to chain ; remove transactions within it from incompl_transxns; notify the others.
        if validity:
            self.incompl_transxns = [transxn for transxn in self.incompl_transxns if transxn not in block.transxns]
            self.my_incompl_transxns = [transxn for transxn in self.my_incompl_transxns if transxn not in block.transxns]
            new_block = Block(copyBlock=block)
            self.chain.append(new_block)
        return
    
    def newNode(self):
        '''
        Creates and appends new node to blockchain's node property
        -
        Returns: Node
        '''
        new_node = Node( nds = self.nodes[:], chain = self.chain[:], inctrnsxns = self.incompl_transxns[:], CBVal=self.CBVal)
        self.notifyNodes(data=new_node, newNode=True)
        return new_node
    
    def newTransaction(self, transxn):
        ''' 
        Appends attached transaction to list of uncompleted transaction, and notifies other nodes.
        '''
        self.notifyNodes(data=transxn, newTransxn=True)

    def getByTXID(self,txid):
        for block in self.chain:
            for txn in block.transxns:
                if txn.TXID==txid:
                    return txn
        for txn in self.incompl_transxns:
            if txn.TXID==txid:
                return txn

class Block:
    def __init__(self, copyBlock=None, ph="", t=[], n=None, _time=None, isGenesis=False, minerAdd="", CBVal=None):
        '''
        Constructor. 
        - copyBlock (Block): Block to be directly copied.
        - ph (String): Previous Hash
        - t (Transaction[]): Transactions stored or to-be-stored in the block
        - n (any): Nonce. Only use it as a parameter to configure the Genesis Block
        - _time (any): Timestamp
        - isGenesis (boolean) : is the Genesis block?
        - minerAdd (string): Miner's address, used for Coinbase Transaction and deleted after.
        - CBVal (number): Coinbase value; reward for mine as determined by Blockchain's logic. Only feed in BC attribute.
        '''
        
        if copyBlock:
            cb = copyBlock
            self.set_constructor_vals(ph=cb.prevHash, mr=cb.merkleRoot, _time=cb.timestamp, n=cb.nonce, t=cb.transxns, minerAdd = cb.minerAdd, CBVal = cb.CBVal, MBS=cb.maxBlockSize, hash=cb.hash)
        else:
            self.set_constructor_vals(ph=ph, t=t, n=n, _time=_time, isGenesis=isGenesis, minerAdd=minerAdd, CBVal=CBVal)

    def set_constructor_vals(self, ph="", mr=None, t=[], n=None, _time=None, isGenesis=False, minerAdd="", CBVal=None, MBS=5, hash=None):
        '''Header: '''
        self.prevHash = ph #: string
        self.merkleRoot = mr #: string
        self.timestamp = _time if _time else time.time()
        self.nonce = n #: number | string (for GenesisBlock)

        ''' Body: '''
        self.transxns = t #: Transaction[]

        ''' Other: '''
        self.minerAdd = minerAdd #: string
        self.CBVal = CBVal #: number
        self.maxBlockSize = MBS #[limit] on # txns

        ''' HASH '''
        self.hash = self.getGenesisHash() if isGenesis else hash

    # def __repr__(self):
    #     return str(vars(self))

    def getGenesisHash(self):
        encrypter = SHA256.new()
        encrypter.update(self.nonce)
        return encrypter.hexdigest()

    def setTransactions(self, t=[]):
        self.transxns = t

    def proofOfWork(self, _print=False):
        ''' 
        Proof of Work function. Constructs Merkle Root, then compiles data into Header, then iterates over nonce until
        satisfying condition.
        - Returns: nonce (number)
        '''
        merkleRoot, prevHash, timestamp, nonce = self.getMerkleRoot(), self.prevHash, self.timestamp, 0
        encrypter = SHA256.new()

        potlHash = ""
        while(potlHash[0:3]!="000"):
            encrypter.update(merkleRoot+prevHash+str(timestamp)+str(nonce))
            potlHash = encrypter.hexdigest()
            nonce+=1

        self.hash = potlHash
        self.nonce = nonce
        if _print:
            print("POW Success; nonce = ", nonce, "; hash = ",potlHash)
        # then hash the Merkle Tree; the Nonce; and the Prev. Hash all together.
        return 
    
    def formatMerkleTree(self, transactions):
        '''
        Helper function of getMerkleRoot used to ensure that transactions array fits into binary hash
        tree structure and to provide a helpful indexed list to allow us to more easily prevent re-calculation
        of the same hashes.
         - transactions (Transaction[]): The list of the transactions to be formatted
        Returns: (
            formattedTransactions (Transaction[]): Now compatible with Binary Hash Tree structure,  
            indexedTransactions (Number[]): 0-indexed list where index=value of len(formattedTransactions)
        )
        '''
        if transactions:
            indexed_transxns = range(len(transactions))
            height = int(math.ceil(math.log( len(transactions) , 2 )))
            num_txns_required = 2**height
            right_leaves_occupied = int(len(transactions) - 2**(height-1))
            oddFlag = right_leaves_occupied%2
            if oddFlag:
                while(len(transactions) < num_txns_required):
                    transactions += transactions[-2:]
                    indexed_transxns += indexed_transxns[-2:]
            else:
                while(len(transactions) < num_txns_required):
                    transactions.append(transactions[-1])
                    indexed_transxns.append(indexed_transxns[-1])
        return (transactions, indexed_transxns)
    
    def getMerkleRoot(self):
        '''
        Generates the Merkle Root for the header of the Block based on the included transactions
         - Returns: (string)     
         Stores value (string) in merkleRoot variable.  
        '''
        
        ''' Step 1) Make local copy of transactions '''
        transaction_list = self.transxns[:]
        
        ''' Step 2) Run all transactions through hash to generate Leaf-Node level'''
        h1 = SHA256.new()
        hashed_transaction_list = []
        for transxn in transaction_list:
            h1.update(transxn.toString())
            hashed_transaction_list+=[h1.hexdigest()]
        
        ''' Step 3) Format Tree'''
        (merkle_tree_leaves, merkle_tree_leaves_indexes) = self.formatMerkleTree(hashed_transaction_list[:])

        ''' Step 4) While possible, pair the tree nodes into 2's and hash them. '''
        hashes_iterator = merkle_tree_leaves[:]
        hashes_iterator_indexes = merkle_tree_leaves_indexes[:]
        while len(hashes_iterator)>1:
            hash_pairs = [ hashes_iterator[i:i+2] for i in range(0,len(hashes_iterator),2)]
            hash_index_pairs = [ hashes_iterator_indexes[i:i+2] for i in range(0,len(hashes_iterator_indexes),2)]
            calculated_hash_index_pairs = []
            updated_hashes = []
            for hash_pair, hash_index_pair in zip(hash_pairs,hash_index_pairs):
                if hash_index_pair in calculated_hash_index_pairs:
                    updated_hashes += [ updated_hashes[calculated_hash_index_pairs.index(hash_index_pair)] ]
                else:
                    _hash = "".join(hash_pair) # If we know that this is a list of strings then we don't need to map.
                    # _hash = "".join(map(str, hash_pair))
                    h1.update(_hash)
                    updated_hashes+=[h1.hexdigest()]
                    calculated_hash_index_pairs += [hash_index_pair]
            hashes_iterator = updated_hashes
        # In event of Genesis Node without previous transactions, store arbitrary string insted of empty array
        hashes_iterator = "0" if len(hashes_iterator)==0 else hashes_iterator[0]
        # Store value of Merkle Tree & return it too just in case.
        self.merkleRoot = hashes_iterator
        return hashes_iterator

class Transaction:
    def __init__(self, _cB=False):
        '''
        Constructor.
        '''
        self.header = TransactionHeader()
        self.inputs = [ ] #self.getTransactionInputs()
        self.outputs = [ ] #TransactionOutput[]
        self.coinBase = _cB
        self.TXID = None
        self.timestamp = time.time()

    def getTXID(self):
        encrypter = SHA256.new()
        _str = str(self.header)+str(self.inputs) + str(self.outputs) + str(self.coinBase)+str(self.timestamp)
        encrypter.update(_str)
        _str2 = encrypter.hexdigest()
        encrypter.update(_str2)
        txid = encrypter.hexdigest()
        return txid

    def setTXID(self):
        self.TXID = self.getTXID()

    def __repr__(self):
        return str(vars(self))
    
    def setInputs(self, inputs, pk=None):
        '''
        Takes a list of inputs in convenient format and instantiates TransasctionInputs from them.
         - inputs [ [TXID, N, fxn],... ] : List of all data needed to ID all indvd'l UTXOs we want to use
         - pk (string): Public key of wallet; used to instantiate scriptSig.
        Returns: nothing
        '''
        for inp in inputs:
            txid, n, fxn = inp
            new_inp = TransactionInput(txid, n)
            if not self.coinBase:
                new_inp.scriptSig = scriptSig(pk=pk, PKScriptFxn=fxn)
            self.inputs.append(new_inp)
        self.header.vin_sz = len(inputs)

    def setOutputs(self, outputs):
        '''
        Takes a list of outputs in convenient format and instantiates TransactionOutputs from them.
        - outputs [[#, str]x2?]: Info for Outputs; Ready to be thrown into constructor.
        Returns: nothing
        '''
        for (_val, rcpt_addr) in outputs:
            new_outp = TransactionOutput(_val = _val, rcpt_address = rcpt_addr)
            self.outputs.append(new_outp)
        self.header.vout_sz = len(outputs)

    def toString(self):
        return str(vars(self))

class TransactionHeader:
    ''' 
    A class representing the Header of a Transaction. Used as part of Transaction
    '''
    def __init__(self, _vin=None, _vout=None, _lt=None, __v=1):
        '''
        Constructor.
        - _vin (number): vin_sz; the # of inputs attached.
        - _vout (number): vout_sz; the # of outputs attached.
        - _lt (any): Lock time (?)
        - __v (string): Version number that should be used to verify the block.

        '''
        self.vin_sz = _vin
        self.vout_sz = _vout
        self.lock_time = _lt
        self.ver = __v
    
    def __repr__(self):
        return str(vars(self))

class TransactionInput:
    ''' 
    A class representing an individual Input of a Transaction. Used as part of Transaction.
    '''
    def __init__(self, _txid=None, _n=0, _scriptSig=None):
        '''
        Constructor.
        - _txid (string): the hash pointing to the UTXO which (1) belongs to the sender and (2) is selected for this input
        - _n (number): an index locating the specific UTXO from its Hash 
        - _scriptSig (any): "A 'Spending Script' that proves the creator of the transaction has permission to spend the money referenced."
        '''
        self.TXID = _txid
        self.n = _n
        self.scriptSig = _scriptSig

    def __repr__(self):
        return str(vars(self))

class TransactionOutput:
    ''' 
    A class representing an individual Output of a Transaction. Used as part of Transaction.
    '''
    def __init__(self, _val=None, rcpt_address=""):
        '''
        Constructor.
        - _val (number): value of this output
        '''
        self.val = _val
        self.scriptPubKey = scriptPubKey(rcpt_address)
    
    def __repr__(self):
        return str(vars(self))
    
class scriptPubKey:
    '''
    This the "locking" script, used to lock an Output in the name of a user whose PK hashes to the given address.
    The Verify method is passed into the scriptSig instance so the sender can prove ownership.
    A lock is created simply by passing in the recipient's address.
    '''
    def __init__(self, rcpt_addr=""):
        self.rcpt_address = rcpt_addr #Pub Key Hash
    
    def verify(self, pub_k=None, retAddrInstead=False):
        '''
        Called by the scriptSig of the 'redeeming transaction' to 'unlock' this UTXO. We hash input public_key
        to get a PHKA(address) and ensure that that is the address set out for us.
        - pub_k (string): public key of transaction.
        - retAddrInstead (boolean): True - rets Addr; False - Boolean
        Returns: valid? (retAddrInstead? addr(string): True) : False
        '''
        addr = ConvertPK2Address(pub_k)
        if (pub_k != self.rcpt_address) and (addr==self.rcpt_address):
            if retAddrInstead:
                return addr
            else:
                return True
        return False

    def __repr__(self):
        return str(vars(self))

class scriptSig:
    '''
    This is the "unlocking" script, used to open a UTXO for it to be input to a transaction.
    It takes as input the Public Key Script which was used by the previous sender to 
    lock the Output in this current sender's name. 
    ex: A -> B -> C
    This is B's scriptSig unlocking A's scriptPubKey
    '''
    def __init__(self, pk="", PKScriptFxn=None):
        ''' 
        Constructor.
        - pk (string): Public Key
        - PKScriptFxn (function): Verify method of scriptPubKey instance
        '''
        self.public_key = pk 
        self.PKScriptFxn = PKScriptFxn
        (self.verified, self.address) = self.verify()

    def verify(self):
        if self.PKScriptFxn:
            verified_add = self.PKScriptFxn(pub_k = self.public_key, retAddrInstead=True)
            return (True, verified_add) if verified_add else (False, None)
        else:
            print 'PKScript function is none?'

    def __repr__(self):
        return str(vars(self))

class Node:
    '''
    Node class with wallet and ability-to-mine built in.
    '''
    def __init__(self, nds=[],chain=[],inctrnsxns=[], CBVal=None):
        '''
        Constructor.
        This method should only be called manually when you create NodePoE. In all other circumstances, 
        the correct way to instantiate a node is to call BlockchainPoE's newNode. This automatically feeds it
        a 'Snapshot' of BlockchainPoE's data so this Node can create a BC with correct starting values.
        When manually calling to create NodePoE, can set initial CB Value & other BC configurations.
        - nds (Node[]): list of the other nodes tuned into BC at that given point of time
        - chain (Block[]): list of blocks comprising the blockchain
        - inctrnsxns (Transaction[]): list of incomplete transactions to be added to the Blockchain, thereafter made into Blocks
        - CBVal (Transaction[]): Coinbase Value. In'l CBVal set thru instantiation of NodePoE in script.py
        '''
        self.blockchain = Blockchain(nds, chain, inctrnsxns, CBval=CBVal) #: Blockchain
        self.wallet = Wallet(self.blockchain)
    
    def __repr__(self):
        return str(vars(self))

    # Keeping up-to-date:
    def updateInfo(self, data=None, newNode=False, newBlock=False, newTransxn=False, newCBVal=False):
        if newNode:
            self.blockchain.nodes.append(data) #Pass by Reference
        elif newCBVal:
            self.blockchain.CBVal = newCBVal 
        elif newTransxn:
            verified = self.verifyTransaction(data)
            if verified:
                self.blockchain.incompl_transxns.append(data)
        elif newBlock:
            verified = self.verifyBlock(data) #Pass by Value
            if verified:
                self.blockchain.newBlock(data)
        return

    def verifyBlock(self, block = None):
        '''
        Function to run tests, determining validity of block. Documentation w/in fxn.
        - block (Block): block that we are verifying
        Return: boolean
        '''
        return True

    def verifyTransaction(self, txn = None):
        '''
        Function to run tests, determining validity of Transaction. Documentation w/in fxn.
        Note: COINBASE TRANSACTIONS ARE NOT PASSED IN HERE
        - txn (Transaction): transaction that we are verifying
        Return: boolean
        '''

        #1) Make sure neither transaction Input nor transaction Output list is empty
        test1 = txn.inputs and txn.outputs
        if not test1:
            print "Test1 failed"
            return False
        #2) Make sure none of the Inputs have hash=0, n=-1; these are reserved for Coinbase
        test2 = self.__notCBTxn(txn)
        if not test2:
            print "Test2 failed"
            return False

        #3) sum(Input) >= sum(Output)
        test3 = self.__inputsAreGrequalOutputs(txn)
        if not test3:
            print "Test3 failed"
            return False

        #4) Make sure the Output referenced as Input is not used elsewhere.
        test4 = self.__inputsAreUtxos(txn)
        if not test4:
            print "Test4 failed"
            return False

        #5) Ensure ScriptSigs are verified.
        for inp in txn.inputs:
            if not inp.scriptSig.verified:
                print "Test5 failed"
                return False
        
        return True

    #Mining:
    def mine(self, _print=False):
        '''
        Create and then mine a new block.
        INCOMPLETE
        '''
        #To mine, you:
        #1) Create a new block.
        _ph = "" if len(self.blockchain.chain)==0 else self.blockchain.chain[-1].hash

        block = Block(ph=_ph)
        
        #2) Select a subset of the BC's incomplete transactions
        max_number_transxns = block.maxBlockSize #Arbitrary for Demo purposes; sync up max-Block-Size & Transxn Size
        selected_txns = self.selectTransxns(max_number_transxns)

        #3) Feed it the incomplete transactions      
        block.setTransactions(selected_txns)

        #4) Perform Proof of Work.
        block.proofOfWork(_print=_print)

        #5) Broadcast it to the other nodes.
        self.blockchain.notifyNodes(data=block, newBlock=True)

        return block
    
    def selectTransxns(self, max_number):
        '''
        Select Incomplete Transactions to be included in Block when you mine it; generates Coinbase Transaction
        - max_number (number): max # TRANSXNS that fit in a Block (MVP version).
        Returns: (Transaction[]) transactions to include in Block.
        '''
        cbT = self.genCoinbaseTransxn()
        return [cbT]+self.blockchain.incompl_transxns[ 0 : (max_number-1) ]

    def genCoinbaseTransxn(self):
        ''' 
        Creates Coinbase Transaction. Called only by selectTransxns.
        - Returns: (Transaction) cbTransxn
        '''
        cbTransxn = None
        cbTransxn = Transaction(_cB=True)
        cbTransxn.setInputs( inputs=[[0,-1, None]], pk=None )
        cbTransxn.setOutputs( [ [self.blockchain.CBVal, self.wallet.address] ] )
        cbTransxn.setTXID()
        return cbTransxn

    
    #Helper fucntions:
    def __notCBTxn(self, txn = None):
        '''
        Helper function to satisfy test#2 of self.verifyTransaction(*)
        No Input should have hash=0, n=-1; these are reserved for Coinbase transaction.
        - txn (Transaction): The transaction we test
        Return: boolean 
        '''
        for inp in txn.inputs:
            if (inp.TXID == "0") and (inp.n == -1):
                return False
        return True

    def __inputsAreGrequalOutputs(self, txn = None):
        #Must throw this in with the other pending transactions so we can get output value.
        inputs_pairs = []
        input_val = 0
        output_val = self.__getOutputVal(txn)
        for inp in txn.inputs:
            inputs_pairs.append([inp.TXID, inp.n])

        for block in self.wallet.blockchain.chain:
            for txn in block.transxns:
                for i in range(len(txn.outputs)):
                    outp_id = [txn.TXID, i]
                    if outp_id in inputs_pairs: #If 1 of txn's Inputs are found as Output of another txn, its UTXO.
                        input_val += txn.outputs[i].val
                        inputs_pairs.remove(outp_id)
                        if ((len(inputs_pairs)==0) and (input_val>=output_val)):
                            return True
        
        for txn in self.blockchain.incompl_transxns:
            for i in range(len(txn.outputs)):
                outp_id = [txn.TXID, i]
                if outp_id in inputs_pairs: #If 1 of txn's Inputs are found as Output of another txn, its UTXO.
                    input_val += txn.outputs[i].val
                    inputs_pairs.remove(outp_id)
                    if ((len(inputs_pairs)==0) and (input_val>=output_val)):
                        return True
        
    def __inputsAreUtxos(self, txn = None):
        '''
        Helper function to satisfy tests#4 of self.verifyTransaction(*)
        Given transaction, extract IDs of Inputs, confirm these IDs refer to existing Outputs and were never used as Inputs
        Moving backwards thru BC, if we don't see the Spending of a transaction before its Creation, then its a UTXO.
        Sum of Inputs must all be greater than or equal to sum of Outputs
        - txn (Transaction): The transaction we test
        Return: boolean 
        '''
        inputs_pairs = [] #<[(TXID, n)]>; list of input IDs
        for inp in txn.inputs:
            inputs_pairs.append([inp.TXID, inp.n])

        for block in self.wallet.blockchain.chain[:]:
            for txn in block.transxns:
                for inp in txn.inputs:
                    inp_id = [inp.TXID, inp.n]
                    if inp_id in inputs_pairs: #If 1 of txn's Inputs are used as inputs to another txn, reject.
                        return False
                
                for i in range(len(txn.outputs)):
                    outp_id = [txn.TXID, i]
                    if outp_id in inputs_pairs: #If 1 of txn's Inputs are found as Output of another txn, its UTXO.
                        inputs_pairs.remove(outp_id)
                        if ((len(inputs_pairs)==0)):
                            return True
        
        for txn in self.blockchain.incompl_transxns:
            for inp in txn.inputs:
                inp_id = [inp.TXID, inp.n]
                if inp_id in inputs_pairs: #If 1 of txn's Inputs are used as inputs to another txn, reject.
                    return False

            for i in range(len(txn.outputs)):
                outp_id = [txn.TXID, i]
                if outp_id in inputs_pairs: #If 1 of txn's Inputs are found as Output of another txn, its UTXO.
                    inputs_pairs.remove(outp_id)
                    if ((len(inputs_pairs)==0)):
                        return True
        
        return False
    
    def __getOutputVal(self, txn = None):
        return sum([outp.val for outp in txn.outputs])

class Wallet:
    def __init__(self, bc):
        self.public_key, self.private_key = self.genKeys() #: string
        self.address = ConvertPK2Address(self.public_key)
        self.blockchain = bc
    
    def __repr__(self):
        return str(vars(self))
    
    def genKeys(self):
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        public_key = public_key
        private_key = private_key
        return [public_key, private_key]
    
    def getIncompleteUTXOInfo(self, val=0,getAll=False, getArrs=True):
        val_found = 0
        STXOs, UTXOs = [], [] #Spent Transaction Outputs; Unspent Transaction Outputs
        addr = self.address

        for txn in self.blockchain.my_incompl_transxns[::-1]:
            for inp in txn.inputs:
                if (txn.coinBase==False and inp.scriptSig.address==addr):
                    STXOs.append( [ inp.TXID, inp.n ] )
                else:
                    continue
            i = 0
            for outp in txn.outputs:
                if outp.scriptPubKey.rcpt_address==addr:
                    # If it is in the STXOs, do nothing
                    if ( [txn.TXID, i] in STXOs):
                        continue   
                    else:
                        #append it to UTXO & add val_found.
                        UTXOs.append( [txn.TXID, i, outp.scriptPubKey.verify] )
                        val_found += outp.val
                        if (not getAll) and (val_found >= val):
                            if(getArrs):
                                return (UTXOs, val_found, STXOs)
                            else:
                                return (UTXOs, val_found)
                i +=1
        if(getArrs):
            return ( UTXOs, val_found, STXOs)
        else:
            return (UTXOs, val_found)

    def getUTXOs(self, val=0, getAll=False):
        '''
        Get Ununused Transaction Outputs by iterating backwards (last-first) through BC, checking 
        transactions' Inputs and Outputs for instances of the address. 
        If an Input is found that has this wallet's address in its signature, then we store the TXID & Index
        that determine that input in STXO, so we know not to count the Output should we find it.
        If an Output is found that has this wallet's address in the ScriptPubKey, then we add the value of that
        individual output to the composite and add its identifying (TXID, N) to the UTXOs list.
        We exit if we complete the Blockchain OR get at least the value required
        - val (number): The Satoshi value of currency needed for transaction.
        - getAll (boolean): Get all UTXOs?
        Returns ( [ [TXID, N, PublicKeySig],... ] , number ) | ( None, None ) : (UTXOs, value)
        '''
        #1) Declare some vars to help us:
        val_found = 0
        STXOs, UTXOs = [], [] #Spent Transaction Outputs; Unspent Transaction Outputs
        addr = self.address

        UTXOs, val_found, STXOs = self.getIncompleteUTXOInfo(val=val, getAll=getAll, getArrs=True)
        if (not getAll) and (val_found>=val):
            return (UTXOs, val_found)

        #2) Loop over Blockchain, working through each part of each transaction of each block
        # until either the BC finishes or we meet our condition.
        for block in self.blockchain.chain[::-1]:
            for txn in block.transxns[::-1]:
                #A) See if address spends any UTXOs in this transaction's Inputs array; if so, record that UTXO's ID:
                for inp in txn.inputs:
                    if (txn.coinBase==False and inp.scriptSig.address==addr):
                        STXOs.append( [ inp.TXID, inp.n ] )
                    else:
                        continue
                
                #B) See if address in in Outputs array
                i = 0
                for outp in txn.outputs:
                    if outp.scriptPubKey.rcpt_address==addr:
                        # If it is in the STXOs, do nothing
                        if ( [txn.TXID, i] in STXOs):
                            continue   
                        else:
                            #append it to UTXO & add val_found.
                            UTXOs.append( [txn.TXID, i, outp.scriptPubKey.verify] )
                            val_found += outp.val
                            if (not getAll) and (val_found >= val):
                                return (UTXOs, val_found)
                    i+=1
        if val_found>=val:
            return (UTXOs, val_found)
        return (None, None)

    def outputsHelper(self, val=None, UTXO_val=None, rcpt_address=False):
        '''
        Function that takes in a value and returns an array that has 2 arrays; each
        will be the inputs to the TransactionOutput constructor: 1 for the payment, 
        going to rcpt_address; the other for change, going to my address. This is an
        intermediary step, called by makeTransaction; the vals from here will be passed
        on to the transaction.
        - val (number): The Satoshi amount you want to send as a payment
        - UTXO_val (number): The total Satoshi value of the UTXOs
        - rcpt_address (string): The address you want to send your payment to
        Returns [ [val, rcpt_address], [val, my_address] ]
        '''
        if UTXO_val > val:
            return [ [val, rcpt_address], [UTXO_val - val, self.address] ]
        else:
            return [ [val, rcpt_address] ]

    def makeTransaction(self, rcpt_address, val, _print=True):
        '''
        Make transaction from this wallet to recepient's address of certain value.
        - rcpt_address (string): address of recipient
        - val (number): Satoshi amount you wish to send.
        Returns: Transaction (for now)
        '''
        # 1) Create new instance of Transaction class
        transxn = Transaction()

        # 2) Get only enough UTXO to complete transaction. Pass them, in a convenient format, to the Transaction obj to set them as its Input.
        (UTXOs, UTXO_val) = self.getUTXOs(val=val, getAll=False) 
        if not UTXOs:
            if _print:
                print "Insufficient Funds. Transaction cancelled."
            return
        transxn.setInputs(UTXOs, self.public_key)

        # 3) Take the UTXO_val and break it into Payment & Change, then pass that, in a convenient format, to the Transaction ob to 
        #   set them as Output.
        transxn.setOutputs(self.outputsHelper(val=val, UTXO_val=UTXO_val, rcpt_address=rcpt_address ))

        # 4) Once done setting the Transaction's inner values, set the TXID.
        transxn.setTXID()
        self.blockchain.my_incompl_transxns.append(transxn)

        # 4) Once the Transaction's Inputs & Outputs are set, then we want to notify the other nodes.
        # Note: The process for nodes to verify transactions hasn't been built out yet.
        self.blockchain.notifyNodes(data=transxn, newTransxn=True)

        if _print:
            print "Successful transaction."
        return transxn

    def getBalance(self):
        return self.getUTXOs(getAll=True)[1]

''' Global functions '''

def ConvertPK2Address(pub_key):
    '''
    Converts Public Key to Address
    - pub-key (string): Public Key
    Returns (string): address
    '''
    h1 = SHA256.new()
    h1.update(pub_key)
    h1d = h1.hexdigest()
    #3. Perform RIPEMD-160 hashing on result
    h2 = RIPEMD160.new()
    h2.update(h1d)
    h2d = h2.hexdigest()
    #4. Add version byte in front of RIPEMD-160 hash (0x00 for Main Network
    h2d = b'00'+h2d
    #5. Perform SHA-256 hash on the extended RIPEMD-160 result
    h3 = SHA256.new()
    h3.update(h2d)
    h3d = h3.hexdigest()
    #6. Perform SHA-256 hash on the result of the previous SHA-256 hash
    h4 = SHA256.new()
    h4.update(h3d)
    h4d = h4.hexdigest()
    #7. Take the first 4 bytes of the second SHA-256 hash. This is the address checksum
    _bytes = h4d[:8]
    #8. Add the 4 checksum bytes from stage 7 at the end of extended RIPEMD-160 hash from stage 4. This is the 25-byte binary Bitcoin Address.
    add = h2d+_bytes
    #9. Convert the result from a byte string into a base58 string using Base58Check encoding.
    _c = base58.b58encode(add)
    return _c


