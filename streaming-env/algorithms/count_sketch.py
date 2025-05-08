import random
import hashlib

class BasicCountSketch:
    def __init__(self, width: int, seed: int = 42):
        self.width = width
        self.count = [0] * width
        
        random.seed(seed)
        self.hash_seed = random.randint(0, 2**31 - 1)
        self.sign_seed = random.randint(0, 2**31 - 1)

    def _hash(self, item, seed):
        item = str(item)
        h = hashlib.md5((str(seed) + item).encode())
        return int(h.hexdigest(), 16)

    def _index(self, item):
        return self._hash(item, self.hash_seed) % self.width

    def _sign(self, item):
        return 1 if self._hash(item, self.sign_seed) % 2 == 0 else -1

    def update(self, item, count=1):
        idx = self._index(item)
        sign = self._sign(item)
        self.count[idx] += count * sign

    def estimate(self, item):
        idx = self._index(item)
        sign = self._sign(item)
        return self.count[idx] * sign

    # def __init__(self, width: int, depth: int, seed: int = 42):
    #     """
    #     width: number of counters per row
    #     depth: number of hash functions (rows)
    #     """
    #     self.width = width
    #     self.depth = depth
    #     self.count = [[0] * width for _ in range(depth)]
    #     random.seed(seed)
    #     self.hash_seeds = [random.randint(0, 2**31 - 1) for _ in range(depth)]
    #     self.sign_seeds = [random.randint(0, 2**31 - 1) for _ in range(depth)]

    # def _hash(self, item, seed):
    #     """
    #     General-purpose hash function using hashlib
    #     """
    #     item = str(item)
    #     h = hashlib.md5((str(seed) + item).encode())
    #     return int(h.hexdigest(), 16)

    # def _index(self, item, i):
    #     return self._hash(item, self.hash_seeds[i]) % self.width

    # def _sign(self, item, i):
    #     return 1 if self._hash(item, self.sign_seeds[i]) % 2 == 0 else -1

    # def update(self, item):
    #     for i in range(self.depth):
    #         idx = self._index(item, i)
    #         sign = self._sign(item, i)
    #         self.count[i][idx] += sign

    # def estimate(self, item):
    #     total = 0
    #     for i in range(self.depth):
    #         idx = self._index(item, i)
    #         sign = self._sign(item, i)
    #         total += sign * self.count[i][idx]
    #     return total // self.depth  
