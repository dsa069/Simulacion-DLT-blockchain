class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce, merkle_root):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.merkle_root = merkle_root
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        import hashlib
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}{self.merkle_root}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __repr__(self):
        return f"Block(Index: {self.index}, Hash: {self.hash}, Previous Hash: {self.previous_hash})"