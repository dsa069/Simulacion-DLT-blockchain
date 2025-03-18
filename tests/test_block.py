import unittest
from src.block import Block
from src.utils.hash_utils import hash_data
from src.utils.timestamp import get_current_timestamp

class TestBlock(unittest.TestCase):

    def setUp(self):
        self.previous_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        self.timestamp = get_current_timestamp()
        self.data = "Test transaction data"
        self.nonce = 0
        self.block = Block(index=1, previous_hash=self.previous_hash, timestamp=self.timestamp, data=self.data, nonce=self.nonce)

    def test_block_creation(self):
        self.assertEqual(self.block.index, 1)
        self.assertEqual(self.block.previous_hash, self.previous_hash)
        self.assertEqual(self.block.timestamp, self.timestamp)
        self.assertEqual(self.block.data, self.data)
        self.assertEqual(self.block.nonce, self.nonce)

    def test_block_hash(self):
        expected_hash = hash_data(f"{self.block.index}{self.block.previous_hash}{self.block.timestamp}{self.block.data}{self.block.nonce}")
        self.assertEqual(self.block.calculate_hash(), expected_hash)

    def test_block_properties(self):
        self.assertIsNotNone(self.block.hash)
        self.assertTrue(self.block.hash.startswith('000'))

if __name__ == '__main__':
    unittest.main()