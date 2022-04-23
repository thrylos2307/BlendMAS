import hashlib
import json
from time import time
from uuid import uuid4
from urllib.parse import urlparse
import requests

"Block class"
class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.all_transactions = []
        self.nodes = set()
        # create the genesis block
        self.new_block(previous_hash=1, proof=100)

    @staticmethod
    def hash(block):
        # hashing block
        gen_hash = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(gen_hash).hexdigest()

    def new_block(self, proof, previous_hash=None):
        # creates a new block in the blockchain
        block = {
            'index': len(self.chain)+1,
            'timestamp': time(),
            'transactions': self.all_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # reset the current list of transactions
        self.all_transactions = []
        self.chain.append(block)
        return block

    @property
    def last_block(self):
        # returns last block in the chain
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount):
        #add new data of transaction
        self.all_transactions.append({
            "sender":sender,
            "recient":recipient,
            "data":amount,
        })
        return int(self.last_block['index'])+1

    def proof_of_work(self, last_proof):
        # find a number p' such as hash(pp') containing leading some zeros where p is the previous p'
        proof = 0
        while self.validate_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def validate_proof(last_proof, proof):
        # validates the proof: does hash(last_proof, proof) contain 3 leading zeroes?
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:3] == "000"

    def register_node(self, address):
        # add a new node to the list of nodes
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def full_chain(self):
        # xxx returns the full chain and a number of blocks
        pass
    
    def valid_chain(self, chain):
        # verify blockchain is valid
        last_block = chain[0]
        current_index = 1
        
        while current_index < len(chain):
            block = chain[current_index]
            # verify hash of the block 
            if block['previous_hash'] != self.hash(last_block):
                return False
            # verify proof of work
            if not self.validate_proof(last_block['proof'], block['proof']):
                return False
        
            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        # this is our Consensus Algorithm, it resolves conflicts by replacing
        # our chain with the longest one in the network.

        neighbours = self.nodes  
        new_chain = None

        # we are only looking for the chains longer than ours
        max_length = len(self.chain)

        # grab and verify chains from all the nodes in our network
        for node in neighbours:

            # we utilize our own api to construct the list of chains :)
            resp = requests.get(f'http://{node}/chain')

            if resp.status_code == 200:

                length = resp.json()['length']
                chain = resp.json()['chain']
                
                # check if the chain is longer and whether the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        
        # replace our chain if we discover a new longer valid chain
        if new_chain:
            self.chain = new_chain
            return True

        return False


