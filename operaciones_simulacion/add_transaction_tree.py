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
def save_block_to_file(block, parent_hash=None, folder="dlt_tree"):
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
        "merkle_root": block.merkle_root,
        "parent_hash": parent_hash,  # Store parent hash for tree structure
        "left_child": None,          # Initialize left child as None
        "right_child": None          # Initialize right child as None
    }
    
    # Write the block data to the file
    with open(filename, 'w') as file:
        json.dump(block_data, file, indent=4)
    
    print(f"Block {block.index} saved to {filename}")
    
    # If there's a parent, update the parent's child references
    if parent_hash:
        update_parent_children(parent_hash, block.hash, folder)

def update_parent_children(parent_hash, child_hash, folder="dlt_tree"):
    """Update a parent block's children references"""
    # Find the parent block file
    parent_files = glob.glob(f"{folder}/block_*_{parent_hash[:8]}.json")
    if not parent_files:
        print(f"Warning: Parent block with hash {parent_hash[:8]} not found")
        return
        
    # Read the parent block
    with open(parent_files[0], 'r') as file:
        parent_data = json.load(file)
    
    # Update the appropriate child reference
    if parent_data["left_child"] is None:
        parent_data["left_child"] = child_hash
    elif parent_data["right_child"] is None:
        parent_data["right_child"] = child_hash
    else:
        print(f"Warning: Parent block {parent_hash[:8]} already has two children")
        return
        
    # Write the updated parent block back to the file
    with open(parent_files[0], 'w') as file:
        json.dump(parent_data, file, indent=4)

def find_next_parent_block(folder="dlt_tree"):
    """Find the next block that can accept a child (breadth-first)"""
    # Get all block files
    block_files = glob.glob(f"{folder}/block_*.json")
    if not block_files:
        return None
    
    # Load all blocks
    blocks = []
    for file in block_files:
        with open(file, 'r') as f:
            block_data = json.load(f)
            blocks.append(block_data)
    
    # Sort by index to ensure breadth-first processing
    blocks.sort(key=lambda x: x["index"])
    
    # Find the first block that has fewer than two children
    for block in blocks:
        if block["left_child"] is None or block["right_child"] is None:
            return block
    
    return None

def validate_blockchain_tree(folder="dlt_tree"):
    """
    Validate all blocks in the blockchain tree.
    Checks that:
    1. Each block's hash is valid
    2. Each block's previous_hash matches its parent's hash
    
    Returns:
        tuple: (is_valid, corrupted_block_index)
    """
    # Get all block files
    block_files = glob.glob(f"{folder}/block_*.json")
    if not block_files:
        print("No blocks found in blockchain")
        return True, None
    
    # Load all blocks
    blocks = {}
    for file in block_files:
        with open(file, 'r') as f:
            try:
                block_data = json.load(f)
                blocks[block_data["hash"]] = block_data
            except json.JSONDecodeError:
                print(f"Error: Corrupted block file {file}")
                return False, None
    
    # Validate each block
    for block_hash, block_data in blocks.items():
        # Recreate block to calculate hash
        temp_block = Block(
            index=block_data["index"],
            timestamp=block_data["timestamp"],
            data=block_data["data"],
            previous_hash=block_data["previous_hash"],
            nonce=block_data["nonce"]
        )
        
        # 1. Verify hash integrity
        calculated_hash = temp_block.calculate_hash()
        if calculated_hash != block_hash:
            print(f"Error: Block {block_data['index']} has invalid hash")
            print(f"  Stored: {block_hash}")
            print(f"  Calculated: {calculated_hash}")
            return False, block_data["index"]
        
        # 2. Verify parent-child relationship (except for genesis)
        if block_data["parent_hash"]:
            if block_data["parent_hash"] != block_data["previous_hash"]:
                print(f"Error: Block {block_data['index']} has mismatched parent and previous hash")
                return False, block_data["index"]
            
            # Verify parent exists and has this block as a child
            parent_hash = block_data["parent_hash"]
            if parent_hash not in blocks:
                print(f"Error: Block {block_data['index']} references non-existent parent")
                return False, block_data["index"]
            
            parent = blocks[parent_hash]
            if (parent["left_child"] != block_hash and 
                parent["right_child"] != block_hash):
                print(f"Error: Block {block_data['index']} claims {parent['index']} as parent, but parent doesn't list it as a child")
                return False, block_data["index"]
    
    # Verify child references (bidirectional integrity)
    for block_hash, block_data in blocks.items():
        # Check left child
        if block_data["left_child"] and block_data["left_child"] in blocks:
            child = blocks[block_data["left_child"]]
            if child["parent_hash"] != block_hash:
                print(f"Error: Left child of block {block_data['index']} doesn't reference it as parent")
                return False, block_data["index"]
        
        # Check right child
        if block_data["right_child"] and block_data["right_child"] in blocks:
            child = blocks[block_data["right_child"]]
            if child["parent_hash"] != block_hash:
                print(f"Error: Right child of block {block_data['index']} doesn't reference it as parent")
                return False, block_data["index"]
    
    return True, None

def print_blockchain_tree(folder="dlt_tree"):
    """Print the blockchain as a tree structure"""
    # Get all block files
    block_files = glob.glob(f"{folder}/block_*.json")
    if not block_files:
        print("No blocks found in blockchain")
        return
        
    # Load all blocks
    blocks = {}
    for file in block_files:
        with open(file, 'r') as f:
            block_data = json.load(f)
            blocks[block_data["hash"]] = block_data
    
    # Find the root (genesis block)
    genesis = None
    for hash, block in blocks.items():
        if block["index"] == 0:
            genesis = block
            break
    
    if not genesis:
        print("Error: Genesis block not found")
        return
    
    # Print the tree recursively
    print("\n=== BLOCKCHAIN TREE STRUCTURE ===")
    print_subtree(blocks, genesis["hash"], "", True)

def print_subtree(blocks, block_hash, prefix, is_last):
    """Recursively print a subtree of the blockchain"""
    if block_hash not in blocks:
        return
        
    block = blocks[block_hash]
    
    # Print the current block
    connector = "└── " if is_last else "├── "
    print(f"{prefix}{connector}Block ({block['index']}) [{block_hash[:8]}...]")
    
    # Prepare prefix for children
    child_prefix = prefix + ("    " if is_last else "│   ")
    
    # Print left child if exists
    if block["left_child"]:
        has_right = block["right_child"] is not None
        print_subtree(blocks, block["left_child"], child_prefix, not has_right)
    
    # Print right child if exists
    if block["right_child"]:
        print_subtree(blocks, block["right_child"], child_prefix, True)

def find_highest_block_index(folder="dlt_tree"):
    """Find the highest block index in the dlt folder"""
    # Original implementation is fine for this purpose
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

def print_block_info(block):
    print(f"Block {block.index} has been added to the blockchain!")
    print(f"Hash: {block.hash}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Timestamp: {block.timestamp}")
    print(f"Nonce: {block.nonce}")
    print(f"Merkle Root: {block.merkle_root}")
    print(f"Data: {block.data}")

def add_single_transaction(transaction_data):
    """Add a single transaction to the blockchain tree"""
    folder = "dlt_tree"
    os.makedirs(folder, exist_ok=True)
    
    # Validate existing blockchain tree before adding new block
    is_valid, corrupted_block = validate_blockchain_tree(folder)
    
    if not is_valid:
        print(f"\n⚠️ ERROR: Blockchain tree is corrupted at block {corrupted_block}")
        print("⚠️ New block will not be added to preserve blockchain integrity")
        print("⚠️ Please restore the blockchain from a valid backup or create a new one")
        return
    
    # Check if blockchain exists
    block_files = glob.glob(f"{folder}/block_*.json")
    
    if not block_files:
        # No blocks exist, create a new blockchain with genesis block
        print("\n=== CREATING NEW BLOCKCHAIN TREE ===")
        blockchain = Blockchain()
        print("Creating and saving genesis block...")
        genesis_block = blockchain.chain[0]
        save_block_to_file(genesis_block, None, folder)
        
        # The genesis block becomes the parent for the first transaction
        parent_block = {
            "hash": genesis_block.hash,
            "index": 0
        }
    else:
        # Blockchain exists and is valid, find a block that can accept children
        print(f"\n✅ Blockchain tree integrity verified")
        parent_block = find_next_parent_block(folder)
        if not parent_block:
            print("Error: No parent block available to accept children")
            return
    
    # Create a new block with the parent's hash
    print(f"\n=== ADDING NEW TRANSACTION AS CHILD OF BLOCK {parent_block['index']} ===")
    
    # Get highest index to ensure unique increasing indices
    highest_index = find_highest_block_index(folder)
    
    new_block = Block(
        index=highest_index + 1,
        timestamp=get_current_timestamp(),
        data=transaction_data,
        previous_hash=parent_block["hash"],  # Link to parent
        nonce=0
    )
    
    # Mine the new block
    proof_of_work = ProofOfWork(difficulty=3)
    print(f"Mining block {new_block.index}...")
    proof_of_work.mine(new_block)
    print_block_info(new_block)
    
    # Save the block with parent reference
    save_block_to_file(new_block, parent_block["hash"], folder)
    
    # Print the tree structure
    print_blockchain_tree(folder)
    print(f"\nTransaction has been added to the blockchain tree and saved to {folder}")

if __name__ == "__main__":
    # Get transaction data from user input
    transaction_data = input("Enter transaction data: ")
    if not transaction_data:
        transaction_data = f"Transaction at {get_current_timestamp()}"
    
    add_single_transaction(transaction_data)