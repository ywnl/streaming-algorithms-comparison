
import random
import hashlib

class CountMinSketch:
    def __init__(self, width: int, depth: int, seed: int = 42, prime: bool = False):
        """
        width: number of counters per row
        depth: number of hash functions (rows)
        """
        self.width = width
        self.depth = depth
        self.count = [[0] * width for _ in range(depth)]
        random.seed(seed)
        mod = 2**31 - 1
        if prime == True:
            mod = 2**61 - 1
        self.hash_seeds = [random.randint(0, mod) for _ in range(depth)]

    def _hash(self, item, i):
        """
        Hash function using built-in hashlib + salt (seed)
        """
        item = str(item)
        h = hashlib.md5((str(self.hash_seeds[i]) + item).encode())
        return int(h.hexdigest(), 16) % self.width

    def update(self, item):
        """
        Process an item by incrementing counters across all hash rows.
        """
        for i in range(self.depth):
            index = self._hash(item, i)
            self.count[i][index] += 1

    def estimate(self, item):
        """
        Return the minimum counter value across all hash functions.
        """
        return min(self.count[i][self._hash(item, i)] for i in range(self.depth))


    # def __init__(self, rows, cols, prime = 2**61 - 1):
    #     """
    #     rows: number of hash tables
    #     cols: number of buckets
    #     sketch: linear sketch where element is each hash table
    #     prime: large prime number to avoid collisions
    #     """

    #     self.rows = rows
    #     self.cols = cols
    #     self.sketch = [[0] * cols for _ in range(rows)]
    #     self.prime = prime
    #     self.hash_params = []
    #     for _ in range(rows):
    #         a = random.randint(1, prime-1)
    #         b = random.randint(0, prime-1)
    #         self.hash_params.append((a, b))

    # def __hash__(self, x, i):
    #     """
    #     x: item
    #     i: hash table index
    #     Calculate and return hash value
    #     """

    #     a, b = self.hash_params[i]

    #     return ((a * x + b) % self.prime) % self.cols

    # def insert(self, x, count = 1):
    #     """
    #     x: item
    #     count: count of item
    #     Insert item into the sketch
    #     """
    #     for i in range(self.rows):
    #         h = self.__hash__(x, i)
    #         self.sketch[i][h] += count

    # def delete(self, x, count = 1):
    #     """
    #     x: item
    #     count: count of item (here, just 1)
    #     Delete item from the sketch only if the count is greater than 0
    #     """
    #     for i in range(self.rows):
    #         h = self.__hash__(x, i)
    #         if self.sketch[i][h] > 0:
    #             self.sketch[i][h] -= count

    # def query(self, x):
    #     """
    #     Return the minimum count estimate for item x across all hash functions
    #     """
    #     estimates = []
    #     for i in range(self.rows):
    #         h = self.__hash__(x, i)
    #         estimates.append(self.sketch[i][h])
    #     return min(estimates)
    

    # def __init__(self, rows, cols, n, prime = 2**61 - 1):
    #     """
    #     rows: number of hash tables
    #     cols: number of buckets
    #     sketch: linear sketch where element is each hash table
    #     prime: large prime number to avoid collisions
    #     n: fixed length of string
    #     """

    #     self.rows = rows
    #     self.cols = cols
    #     self.sketch = [[0] * cols for _ in range(rows)]
    #     self.prime = prime
    #     self.n = n
    #     self.hash_params = []
    #     for _ in range(rows):
    #         rand_int = [random.randint(1, prime-1) for i in range(n - 1)]
    #         b = random.randint(0, prime-1)
    #         rand_int.append(b)
    #         self.hash_params.append(tuple(rand_int))

    # def __hash__(self, x, i):
    #     """
    #     x: item
    #     i: hash table index
    #     Calculate and return hash value
    #     """

    #     params = self.hash_params[i]
    #     total = 0

    #     for i in range(len(x)):
    #         total += ord(x[i]) * params[i]
    #     return  (total % self.prime) % self.cols

    # def insert(self, x, count = 1):
    #     """
    #     x: item
    #     count: count of item
    #     Insert item into the sketch
    #     """

    #     if len(x) > self.n:
    #         x = x[:self.n]

    #     for i in range(self.rows):
    #         h = self.__hash__(x, i)
    #         self.sketch[i][h] += count

    # def delete(self, x, count = 1):
    #     """
    #     x: item
    #     count: count of item (here, just 1)
    #     Delete item from the sketch only if the count is greater than 0
    #     """
    #     for i in range(self.rows):
    #         h = self.__hash__(x, i)
    #         if self.sketch[i][h] > 0:
    #             self.sketch[i][h] -= count

    # def query(self, x):
    #     """
    #     Return the minimum count estimate for item x across all hash functions
    #     """
    #     estimates = []
    #     for i in range(self.rows):
    #         h = self.__hash__(x, i)
    #         estimates.append(self.sketch[i][h])
    #     return min(estimates)
