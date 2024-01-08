from hashlib import md5

class StringHasher:
    def hash(str):
        return md5(str.encode()).hexdigest()
