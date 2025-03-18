from datetime import datetime
import random
from src.blockchain import Blockchain
from src.proof_of_work import ProofOfWork
from src.utils.timestamp import get_current_timestamp

def create_transaction(data):
    blockchain = Blockchain()
    proof_of_work = ProofOfWork()

    # Create a new block with the transaction data
    timestamp = get_current_timestamp()
    nonce = random.randint(0, 1000000)  # Random nonce for demonstration
    previous_hash = blockchain.get_last_block().hash if blockchain.chain else '0' * 64

    # Create the Merkle tree and get the Merkle root
    merkle_tree = MerkleTree([data])
    merkle_root = merkle_tree.get_merkle_root()

    # Append the new block to the blockchain
    new_block = blockchain.append_block(data, previous_hash, timestamp, nonce, merkle_root)

    # Perform proof of work
    proof_of_work.mine(new_block)

    print(f"Block {new_block.index} has been added to the blockchain!")
    print(f"Hash: {new_block.hash}")
    print(f"Previous Hash: {previous_hash}")
    print(f"Timestamp: {timestamp}")
    print(f"Nonce: {nonce}")
    print(f"Merkle Root: {merkle_root}")

if __name__ == "__main__":
    transaction_data = "Sample transaction data"
    create_transaction(transaction_data)