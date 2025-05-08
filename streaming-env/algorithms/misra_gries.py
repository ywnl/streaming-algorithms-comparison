class MisraGries:
    def __init__(self, k: int): 
        """
        Initialize
        """
        self.k = k
        self.counters = {}

    def update(self, item):
        """
        Process an item from the stream.
        """
        if item in self.counters:
            self.counters[item] += 1
        elif len(self.counters) < self.k - 1:
            self.counters[item] = 1
        else:
            to_delete = []
            for key in self.counters:
                self.counters[key] -= 1
                if self.counters[key] == 0:
                    to_delete.append(key)
            for key in to_delete:
                del self.counters[key]

    def get_counts(self):
        """
        Return current counters (underestimates possible).
        """
        return self.counters.copy()

    def estimate(self, item):
        """
        Return estimated frequency (will be <= true count).
        """
        return self.counters.get(item, 0)
