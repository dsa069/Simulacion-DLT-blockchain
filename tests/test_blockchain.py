import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.blockchain import Blockchain
from src.proof_of_work import ProofOfWork

class TestBlockchain(unittest.TestCase):

    def setUp(self):
        self.blockchain = Blockchain()
        self.pow = ProofOfWork(difficulty=3)

    def test_genesis_block(self):
        # Test that the blockchain is created with a genesis block
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].index, 0)
        self.assertEqual(self.blockchain.chain[0].data, "Genesis Block")

    def test_append_block(self):
        initial_length = len(self.blockchain.chain)
        data = "Test transaction data"
        self.blockchain.append_block(data)
        self.assertEqual(len(self.blockchain.chain), initial_length + 1)
        self.assertEqual(self.blockchain.chain[-1].data, data)

    def test_blockchain_integrity(self):
        # Add a block and make sure its previous_hash points to the hash of the previous block
        self.blockchain.append_block("First block")
        first_block = self.blockchain.chain[1]
        genesis_block = self.blockchain.chain[0]
        self.assertEqual(first_block.previous_hash, genesis_block.hash)

    def test_proof_of_work(self):
        # Test that mining creates a hash with the required difficulty
        self.blockchain.append_block("Test block")
        block = self.blockchain.chain[-1]
        self.pow.mine(block)
        self.assertTrue(block.hash.startswith('0' * self.pow.difficulty))

if __name__ == '__main__':
    unittest.main()