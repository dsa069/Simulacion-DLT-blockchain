import hashlib

class ProofOfWork:
    def __init__(self, difficulty=3):
        self.difficulty = difficulty
        self.target = '0' * difficulty
        
    def mine(self, block):
        while not self.is_valid(block):
            block.nonce += 1
            block.update_hash()
        return block
        
    def is_valid(self, block):
        return block.hash.startswith(self.target)