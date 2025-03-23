import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.merkle_tree import MerkleTree

class TestMerkleTree(unittest.TestCase):

    def test_merkle_tree_creation(self):
        transactions = ["tx1", "tx2", "tx3", "tx4"]
        merkle_tree = MerkleTree(transactions)
        self.assertIsNotNone(merkle_tree.get_root())

    def test_merkle_tree_with_single_transaction(self):
        transactions = ["tx1"]
        merkle_tree = MerkleTree(transactions)
        self.assertIsNotNone(merkle_tree.get_root())
        
        # For a single transaction, the leaves are duplicated
        # So the root is hash(hash(tx1) + hash(tx1))
        tx_hash = merkle_tree.hash_transaction("tx1")
        expected_root = merkle_tree.hash_pair(tx_hash, tx_hash)
        self.assertEqual(merkle_tree.get_root(), expected_root)

    def test_merkle_tree_with_even_transactions(self):
        transactions = ["tx1", "tx2", "tx3", "tx4"]
        merkle_tree = MerkleTree(transactions)
        self.assertIsNotNone(merkle_tree.get_root())
        self.assertEqual(len(merkle_tree.tree), 3)  # Leaf level + 2 more levels

    def test_merkle_tree_with_odd_transactions(self):
        transactions = ["tx1", "tx2", "tx3"]
        merkle_tree = MerkleTree(transactions)
        self.assertIsNotNone(merkle_tree.get_root())
        # With 3 transactions, the last one gets duplicated
        self.assertEqual(len(merkle_tree.tree[0]), 4)

    def get_current_timestamp():
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat() + 'Z'

if __name__ == '__main__':
    unittest.main()