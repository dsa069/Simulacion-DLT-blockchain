import hashlib
import json
from .merkle_tree import MerkleTree
from .utils.timestamp import get_current_timestamp

class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.merkle_tree = MerkleTree([data]) if data else MerkleTree(["Genesis"])
        self.merkle_root = self.merkle_tree.get_root()
        self.hash = self.calculate_hash()
        
    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "merkle_root": self.merkle_root
        }, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()
        
    def update_hash(self):
        self.hash = self.calculate_hash()