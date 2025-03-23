import sys
import os
import random
# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.blockchain import Blockchain
from src.proof_of_work import ProofOfWork
from src.merkle_tree import MerkleTree
from src.utils.timestamp import get_current_timestamp

def create_transaction(data):
    blockchain = Blockchain()
    proof_of_work = ProofOfWork(difficulty=3)  # Specify difficulty

    # Add transaction to blockchain
    blockchain.append_block(data)
    
    # Get the last block
    last_block = blockchain.last_block
    
    # Perform proof of work
    proof_of_work.mine(last_block)

    print(f"Block {last_block.index} has been added to the blockchain!")
    print(f"Hash: {last_block.hash}")
    print(f"Previous Hash: {last_block.previous_hash}")
    print(f"Timestamp: {last_block.timestamp}")
    print(f"Nonce: {last_block.nonce}")
    print(f"Merkle Root: {last_block.merkle_root}")

if __name__ == "__main__":
    transaction_data = "Sample transaction data"
    create_transaction(transaction_data)