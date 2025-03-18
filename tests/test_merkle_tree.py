import unittest
from src.merkle_tree import MerkleTree

class TestMerkleTree(unittest.TestCase):

    def test_merkle_tree_creation(self):
        transactions = ["tx1", "tx2", "tx3", "tx4"]
        merkle_tree = MerkleTree(transactions)
        self.assertEqual(merkle_tree.get_merkle_root(), "expected_merkle_root_hash")

    def test_merkle_tree_with_single_transaction(self):
        transactions = ["tx1"]
        merkle_tree = MerkleTree(transactions)
        self.assertEqual(merkle_tree.get_merkle_root(), "expected_merkle_root_hash_for_single_tx")

    def test_merkle_tree_with_even_transactions(self):
        transactions = ["tx1", "tx2", "tx3", "tx4", "tx5", "tx6"]
        merkle_tree = MerkleTree(transactions)
        self.assertEqual(merkle_tree.get_merkle_root(), "expected_merkle_root_hash_for_even_tx")

    def test_merkle_tree_with_odd_transactions(self):
        transactions = ["tx1", "tx2", "tx3"]
        merkle_tree = MerkleTree(transactions)
        self.assertEqual(merkle_tree.get_merkle_root(), "expected_merkle_root_hash_for_odd_tx")

if __name__ == '__main__':
    unittest.main()