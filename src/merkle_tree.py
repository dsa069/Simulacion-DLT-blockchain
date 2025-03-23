import hashlib
import json

class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.tree = self.build_tree()
        
    def build_tree(self):
        # Convert transactions to hash strings
        leaves = [self.hash_transaction(tx) for tx in self.transactions]
        
        # Ensure even number of leaves by duplicating the last one if needed
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1])
            
        # Build the tree
        tree = [leaves]
        while len(tree[-1]) > 1:
            level = []
            for i in range(0, len(tree[-1]), 2):
                if i + 1 < len(tree[-1]):
                    level.append(self.hash_pair(tree[-1][i], tree[-1][i+1]))
                else:
                    level.append(tree[-1][i])
            tree.append(level)
            
        return tree
        
    def hash_transaction(self, transaction):
        # Convert transaction to a hash
        return hashlib.sha256(json.dumps(transaction, sort_keys=True).encode()).hexdigest()
        
    def hash_pair(self, left, right):
        # Concatenate and hash the pair
        concat = left + right
        return hashlib.sha256(concat.encode()).hexdigest()
        
    def get_root(self):
        if not self.tree or not self.tree[-1]:
            return None
        return self.tree[-1][0]