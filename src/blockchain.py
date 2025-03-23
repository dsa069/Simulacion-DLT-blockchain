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
    
    def is_chain_valid(self):
        """
        Check if the blockchain is valid by verifying each block's hash and previous_hash
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check if current block's hash is valid
            if current_block.hash != current_block.calculate_hash():
                return False
                
            # Check if current block's previous_hash points to previous block's hash
            if current_block.previous_hash != previous_block.hash:
                return False
                
        return True