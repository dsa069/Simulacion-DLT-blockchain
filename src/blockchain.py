class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(previous_hash='1', nonce=0)  # Create the genesis block

    def create_block(self, nonce, previous_hash):
        block = Block(
            index=len(self.chain) + 1,
            previous_hash=previous_hash,
            timestamp=self.get_current_timestamp(),
            data=self.current_transactions,
            nonce=nonce,
            merkle_root=self.calculate_merkle_root(self.current_transactions)
        )
        self.current_transactions = []  # Reset the current transactions
        self.chain.append(block)
        return block

    def append_block(self, data):
        self.current_transactions.append(data)

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.previous_hash != previous.hash:
                return False

            if not current.validate_block():
                return False

        return True

    def get_current_timestamp(self):
        from utils.timestamp import get_current_timestamp
        return get_current_timestamp()

    def calculate_merkle_root(self, transactions):
        from merkle_tree import MerkleTree
        merkle_tree = MerkleTree(transactions)
        return merkle_tree.get_merkle_root()

    @property
    def last_block(self):
        return self.chain[-1] if self.chain else None