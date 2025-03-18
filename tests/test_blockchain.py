import unittest
from src.blockchain import Blockchain
from src.block import Block
from src.utils.hash_utils import hash_data
from src.utils.timestamp import get_current_timestamp

class TestBlockchain(unittest.TestCase):

    def setUp(self):
        self.blockchain = Blockchain()

    def test_append_block(self):
        initial_length = len(self.blockchain.chain)
        data = "Test transaction data"
        self.blockchain.append_block(data)
        self.assertEqual(len(self.blockchain.chain), initial_length + 1)

    def test_chain_validity(self):
        self.blockchain.append_block("First block")
        self.blockchain.append_block("Second block")
        self.assertTrue(self.blockchain.is_chain_valid())

    def test_invalid_chain(self):
        self.blockchain.append_block("First block")
        self.blockchain.chain[1].previous_hash = "invalid_hash"
        self.assertFalse(self.blockchain.is_chain_valid())

    def test_block_properties(self):
        data = "Test transaction data"
        self.blockchain.append_block(data)
        block = self.blockchain.chain[-1]
        self.assertEqual(block.data, data)
        self.assertEqual(block.timestamp, get_current_timestamp())
        self.assertTrue(block.hash.startswith('000'))

if __name__ == '__main__':
    unittest.main()