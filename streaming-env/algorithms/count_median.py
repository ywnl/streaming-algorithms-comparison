import random
import hashlib

class CountSketchMedian:
    def __init__(self, width: int, depth: int, seed: int = 42):
        """
        width: number of counters per row
        depth: number of hash functions (rows)
        """
        self.width = width
        self.depth = depth
        self.count = [[0] * width for _ in range(depth)]
        random.seed(seed)
        self.hash_seeds = [random.randint(0, 2**31 - 1) for _ in range(depth)]
        self.sign_seeds = [random.randint(0, 2**31 - 1) for _ in range(depth)]

    def _hash(self, item, seed):
        """
        General-purpose hash function using hashlib
        """
        item = str(item)
        h = hashlib.md5((str(seed) + item).encode())
        return int(h.hexdigest(), 16)

    def _index(self, item, i):
        return self._hash(item, self.hash_seeds[i]) % self.width

    def _sign(self, item, i):
        # Produces ±1 depending on sign hash
        return 1 if self._hash(item, self.sign_seeds[i]) % 2 == 0 else -1

    def update(self, item):
        for i in range(self.depth):
            idx = self._index(item, i)
            sign = self._sign(item, i)
            self.count[i][idx] += sign

    def estimate(self, item):
        ests = []
        for i in range(self.depth):
            idx = self._index(item, i)
            sign = self._sign(item, i)
            ests.append(sign * self.count[i][idx])
        return int(median(ests))

def median(lst):
    sorted_lst = sorted(lst)
    n = len(sorted_lst)
    if n % 2 == 1:
        return sorted_lst[n // 2]
    else:
        return (sorted_lst[n // 2 - 1] + sorted_lst[n // 2]) / 2
