class ProofOfWork:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.prefix_str = '0' * difficulty

    def mine(self, block):
        nonce = 0
        while True:
            block.nonce = nonce
            block_hash = block.calculate_hash()
            if block_hash.startswith(self.prefix_str):
                return block_hash
            nonce += 1