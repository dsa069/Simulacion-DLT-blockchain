import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.block import Block
from src.utils.hash_utils import hash_data
from src.utils.timestamp import get_current_timestamp

class TestBlock(unittest.TestCase):

    def setUp(self):
        self.previous_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        self.timestamp = get_current_timestamp()
        self.data = "Test transaction data"
        self.nonce = 0
        self.block = Block(index=1, timestamp=self.timestamp, data=self.data, previous_hash=self.previous_hash, nonce=self.nonce)

    def test_block_creation(self):
        self.assertEqual(self.block.index, 1)
        self.assertEqual(self.block.previous_hash, self.previous_hash)
        self.assertEqual(self.block.timestamp, self.timestamp)
        self.assertEqual(self.block.data, self.data)
        self.assertEqual(self.block.nonce, self.nonce)

    def test_block_hash(self):
        # Test that the hash is calculated correctly
        original_hash = self.block.hash
        self.block.nonce += 1
        self.block.update_hash()
        self.assertNotEqual(original_hash, self.block.hash)

    def test_merkle_root(self):
        # Test that the merkle root is not None
        self.assertIsNotNone(self.block.merkle_root)

if __name__ == '__main__':
    unittest.main()