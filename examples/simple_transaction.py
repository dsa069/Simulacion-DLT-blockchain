import sys
import os
import random
# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.blockchain import Blockchain
from src.proof_of_work import ProofOfWork
from src.merkle_tree import MerkleTree
from src.utils.timestamp import get_current_timestamp

def create_transactions(data1, data2):
    # Create a single blockchain for both transactions
    blockchain = Blockchain()
    proof_of_work = ProofOfWork(difficulty=3)  # Specify difficulty

    # Process first transaction
    print("\n=== TRANSACTION 1 ===")
    blockchain.append_block(data1)
    block1 = blockchain.last_block
    print(f"Mining block {block1.index}...")
    proof_of_work.mine(block1)
    print_block_info(block1)
    
    # Process second transaction
    print("\n=== TRANSACTION 2 ===")
    blockchain.append_block(data2)
    block2 = blockchain.last_block
    print(f"Mining block {block2.index}...")
    proof_of_work.mine(block2)
    print_block_info(block2)
    
    # Validate the blockchain
    print("\n=== BLOCKCHAIN VALIDATION ===")
    is_valid = blockchain.is_chain_valid() if hasattr(blockchain, 'is_chain_valid') else "Validation method not implemented"
    print(f"Is blockchain valid? {is_valid}")
    
    # Print the full chain
    print("\n=== FULL BLOCKCHAIN ===")
    print(f"Chain length: {len(blockchain.chain)} blocks")
    for i, block in enumerate(blockchain.chain):
        print(f"\nBlock {i}: {'Genesis' if i == 0 else ''}")
        print(f"  Hash: {block.hash}")
        print(f"  Previous Hash: {block.previous_hash}")
        print(f"  Data: {block.data}")

def print_block_info(block):
    print(f"Block {block.index} has been added to the blockchain!")
    print(f"Hash: {block.hash}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Timestamp: {block.timestamp}")
    print(f"Nonce: {block.nonce}")
    print(f"Merkle Root: {block.merkle_root}")

if __name__ == "__main__":
    transaction_data1 = "First transaction: Alice sends 5 coins to Bob"
    transaction_data2 = "Second transaction: Bob sends 2 coins to Charlie"
    create_transactions(transaction_data1, transaction_data2)