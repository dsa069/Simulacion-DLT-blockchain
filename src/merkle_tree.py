class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.root = self.build_tree(transactions)

    def build_tree(self, transactions):
        if len(transactions) == 0:
            return None
        elif len(transactions) == 1:
            return self.hash(transactions[0])

        # Hash the transactions in pairs
        hashed_pairs = []
        for i in range(0, len(transactions), 2):
            if i + 1 < len(transactions):
                hashed_pairs.append(self.hash(transactions[i] + transactions[i + 1]))
            else:
                hashed_pairs.append(self.hash(transactions[i]))

        return self.build_tree(hashed_pairs)

    def hash(self, data):
        import hashlib
        return hashlib.sha256(data.encode()).hexdigest()

    def get_merkle_root(self):
        return self.root