# Blockchain Prototype

This project is a prototype of a simple blockchain implementation in Python. It demonstrates the fundamental concepts of a blockchain, including block creation, proof of work, and Merkle trees.

## Features

- **Blockchain Management**: The `Blockchain` class manages the chain of blocks, allowing for the appending of new blocks and validation of the chain.
- **Block Structure**: Each block contains:
  - Index
  - Previous Hash
  - Timestamp
  - Data
  - Nonce
  - Merkle Root
- **Proof of Work**: The `ProofOfWork` class implements a mining algorithm that requires finding a nonce that results in a hash with a minimum of three leading zeros.
- **Merkle Tree**: The `MerkleTree` class constructs a Merkle tree from transaction data, providing a secure way to verify the integrity of the data.

## Getting Started

### Prerequisites

Make sure you have Python 3.x installed on your machine. You can check your Python version by running:

```
python --version
```

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/microsoft/vscode-remote-try-python.git
   ```

2. Navigate to the project directory:

   ```
   cd blockchain-prototype
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

To create a simple transaction and append it to the blockchain, you can run the example provided in `examples/simple_transaction.py`. This script demonstrates how to use the blockchain prototype.

## Running Tests

To ensure the functionality of the blockchain prototype, you can run the unit tests located in the `tests` directory. Use the following command:

```
pytest tests/
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.