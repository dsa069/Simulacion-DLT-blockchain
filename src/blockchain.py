from .block import Block
from .merkle_tree import MerkleTree
from .utils.timestamp import get_current_timestamp
from .proof_of_work import ProofOfWork

class Blockchain:
    def __init__(self):
        self.chain = []
        genesis_block = self.create_block(previous_hash='000000000000000000000000000000000000000000000000000000000000000', nonce=0)
        
        # Mine the genesis block
        pow = ProofOfWork(difficulty=3)
        pow.mine(genesis_block)
        
    def create_block(self, previous_hash, nonce, data=None):
        block = Block(
            index=len(self.chain),
            timestamp=get_current_timestamp(),
            data=data if data else "Genesis Block",
            previous_hash=previous_hash,
            nonce=nonce
        )
        self.chain.append(block)
        return block
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    def append_block(self, data):
        previous_block = self.last_block
        new_block = Block(
            index=len(self.chain),
            timestamp=get_current_timestamp(),
            data=data,
            previous_hash=previous_block.hash,
            nonce=0
        )
        self.chain.append(new_block)
        return new_block