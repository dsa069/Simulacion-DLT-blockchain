import sys
import os
import json
import glob
# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.blockchain import Blockchain
from src.proof_of_work import ProofOfWork
from src.block import Block
from src.utils.timestamp import get_current_timestamp

# Function to save block data to a file
def save_block_to_file(block, folder="dlt"):
    # Ensure the DLT folder exists
    os.makedirs(folder, exist_ok=True)
    
    # Create a filename with the block index and hash
    filename = f"{folder}/block_{block.index}_{block.hash[:8]}.json"
    
    # Check if this block already exists
    if os.path.exists(filename):
        print(f"Block {block.index} already exists at {filename}")
        return
    
    # Create a serializable representation of the block
    block_data = {
        "index": block.index,
        "hash": block.hash,
        "previous_hash": block.previous_hash,
        "timestamp": block.timestamp,
        "data": block.data,
        "nonce": block.nonce,
        "merkle_root": block.merkle_root
    }
    
    # Write the block data to the file
    with open(filename, 'w') as file:
        json.dump(block_data, file, indent=4)
    
    print(f"Block {block.index} saved to {filename}")

def find_highest_block_index(folder="dlt"):
    """Find the highest block index in the dlt folder"""
    if not os.path.exists(folder):
        return -1
        
    # Get all block files
    block_files = glob.glob(f"{folder}/block_*.json")
    
    if not block_files:
        return -1
        
    # Extract indices from filenames
    indices = []
    for file in block_files:
        try:
            # Format is block_INDEX_HASH.json
            parts = os.path.basename(file).split('_')
            if len(parts) >= 2:
                indices.append(int(parts[1]))
        except (ValueError, IndexError):
            pass
            
    return max(indices) if indices else -1

def validate_blockchain(folder="dlt"):
    """
    Validate all blocks in the blockchain stored in the DLT folder.
    Checks that hashes are valid and that the chain is properly linked.
    
    Returns:
        tuple: (is_valid, first_invalid_block_index)
    """
    # Get all block files sorted by index
    block_files = glob.glob(f"{folder}/block_*.json")
    if not block_files:
        return True, None  # Empty chain is valid
    
    # Sort blocks by index
    blocks_data = []
    for file in block_files:
        try:
            index = int(os.path.basename(file).split('_')[1])
            with open(file, 'r') as f:
                block_data = json.load(f)
            blocks_data.append((index, block_data, file))
        except (ValueError, IndexError, json.JSONDecodeError) as e:
            print(f"Error reading block file {file}: {e}")
            return False, None
    
    # Sort by index
    blocks_data.sort(key=lambda x: x[0])
    
    # Check that indices are continuous starting from 0
    expected_indices = list(range(len(blocks_data)))
    actual_indices = [bd[0] for bd in blocks_data]
    
    if expected_indices != actual_indices:
        print("Error: Blockchain has missing blocks or non-sequential indices")
        for i, (expected, actual) in enumerate(zip(expected_indices, actual_indices)):
            if expected != actual:
                return False, expected
        return False, min(set(expected_indices) - set(actual_indices))
    
    # Validate each block
    for i, (_, block_data, file) in enumerate(blocks_data):
        # Recreate block to calculate hash
        temp_block = Block(
            index=block_data["index"],
            timestamp=block_data["timestamp"],
            data=block_data["data"],
            previous_hash=block_data["previous_hash"],
            nonce=block_data["nonce"]
        )
        
        # Verify hash
        calculated_hash = temp_block.calculate_hash()
        if calculated_hash != block_data["hash"]:
            print(f"Error: Block {block_data['index']} has invalid hash")
            print(f"  Stored: {block_data['hash']}")
            print(f"  Calculated: {calculated_hash}")
            return False, block_data["index"]
        
        # Verify chain linkage (except for genesis block)
        if i > 0:
            previous_block = blocks_data[i-1][1]
            if block_data["previous_hash"] != previous_block["hash"]:
                print(f"Error: Block {block_data['index']} has invalid previous_hash")
                print(f"  Stored previous_hash: {block_data['previous_hash']}")
                print(f"  Expected (previous block's hash): {previous_block['hash']}")
                return False, block_data["index"]
    
    return True, None

def print_blockchain_linear(folder="dlt"):
    """Print the blockchain in a linear format showing block pointers"""
    # Get all block files
    block_files = glob.glob(f"{folder}/block_*.json")
    if not block_files:
        print("No blocks found in blockchain")
        return
        
    # Load and sort all blocks by index
    blocks = []
    for file in block_files:
        with open(file, 'r') as f:
            block_data = json.load(f)
            blocks.append(block_data)
    
    blocks.sort(key=lambda x: x["index"])
    
    # Print the chain
    print("\n=== BLOCKCHAIN LINEAR STRUCTURE ===")
    print("Genesis Block (0) [" + blocks[0]["hash"][:8] + "...]")
    
    for i in range(1, len(blocks)):
        prev_hash = blocks[i]["previous_hash"][:8]
        curr_hash = blocks[i]["hash"][:8]
        print(f"   ↑")
        print(f"   └── Block ({blocks[i]['index']}) [{curr_hash}...] points to [{prev_hash}...]")

def add_single_transaction(transaction_data):
    """Add a single transaction to the blockchain"""
    folder = "dlt"
    os.makedirs(folder, exist_ok=True)
    
    # Validate existing blockchain before adding new block
    is_valid, corrupted_block = validate_blockchain(folder)
    
    if not is_valid:
        print(f"\n⚠️ ERROR: Blockchain is corrupted at block {corrupted_block}")
        print("⚠️ New block will not be added to preserve blockchain integrity")
        print("⚠️ Please restore the blockchain from a valid backup or create a new one")
        return
    
    # Continue with existing code if blockchain is valid
    highest_index = find_highest_block_index(folder)
    
    if highest_index == -1:
        # No blocks exist, create a new blockchain with genesis block
        print("\n=== CREATING NEW BLOCKCHAIN ===")
        blockchain = Blockchain()
        print("Creating and saving genesis block...")
        save_block_to_file(blockchain.chain[0], folder)
        
        # Add the new transaction to the new blockchain
        print("\n=== ADDING NEW TRANSACTION ===")
        blockchain.append_block(transaction_data)
        new_block = blockchain.last_block
    else:
        # Blockchain exists, we need to use the existing chain
        print(f"\n=== BLOCKCHAIN ALREADY EXISTS ===")
        print(f"Found existing blocks up to index {highest_index}")
        print(f"✅ Blockchain integrity verified")
        
        # Load the last block to get its hash
        last_block_files = glob.glob(f"{folder}/block_{highest_index}_*.json")
        if not last_block_files:
            print(f"Error: Could not find block with index {highest_index}")
            return
        
        # Read the last block file
        with open(last_block_files[0], 'r') as file:
            last_block_data = json.load(file)
        
        # Create a new block with the correct index and previous hash
        print("\n=== ADDING NEW TRANSACTION ===")
        new_block = Block(
            index=highest_index + 1,
            timestamp=get_current_timestamp(),
            data=transaction_data,
            previous_hash=last_block_data["hash"],
            nonce=0
        )
    
    # Mine the new block
    proof_of_work = ProofOfWork(difficulty=3)
    print(f"Mining block {new_block.index}...")
    proof_of_work.mine(new_block)
    print_block_info(new_block)
    save_block_to_file(new_block, folder)
    
    print_blockchain_linear(folder)
    print(f"\nTransaction has been added to the blockchain and saved to {folder}")

def print_block_info(block):
    print(f"Block {block.index} has been added to the blockchain!")
    print(f"Hash: {block.hash}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Timestamp: {block.timestamp}")
    print(f"Nonce: {block.nonce}")
    print(f"Merkle Root: {block.merkle_root}")
    print(f"Data: {block.data}")

if __name__ == "__main__":
    # Get transaction data from user input
    transaction_data = input("Enter transaction data: ")
    if not transaction_data:
        transaction_data = f"Transaction at {get_current_timestamp()}"
    
    add_single_transaction(transaction_data)