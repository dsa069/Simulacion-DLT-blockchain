def hash_data(data):
    import hashlib
    return hashlib.sha256(data.encode()).hexdigest()