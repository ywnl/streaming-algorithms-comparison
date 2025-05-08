import random

def generate_stream(distribution='uniform', length=1000, item_pool=10, seed=42):
    random.seed(seed)
    stream = []

    if distribution == 'uniform':
        stream = [random.randint(0, item_pool - 1) for _ in range(length)]

    elif distribution == 'zipf':
        # Higher skew = more head-heavy
        skewed_probs = [1.0 / (i + 1) for i in range(item_pool)]
        total = sum(skewed_probs)
        probs = [p / total for p in skewed_probs]
        items = list(range(item_pool))
        stream = random.choices(items, probs, k=length)

    elif distribution == 'bursty':
        burst_items = [0, 1, 2]
        rest = list(range(3, item_pool))
        for _ in range(length):
            if random.random() < 0.7:
                stream.append(random.choice(burst_items))
            else:
                stream.append(random.choice(rest))
    
    else:
        raise ValueError("Unsupported distribution type")

    return stream
