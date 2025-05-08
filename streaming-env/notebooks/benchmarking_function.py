import sys
sys.path.append('../algorithms')

from misra_gries import MisraGries
from count_min_sketch import CountMinSketch
from count_sketch import BasicCountSketch
from count_median import CountSketchMedian
import time
from collections import Counter


def compute_errors(estimated, true_counts):
    errors = {}
    for item in true_counts:
        true = true_counts[item]
        est = estimated.get(item, 0)
        abs_error = abs(est - true)
        rel_error = abs_error / true if true != 0 else 0
        errors[item] = (true, est, abs_error, rel_error)
    return errors

def evaluate_top_k(true_counts, estimated_counts, k):
    # Get the true and estimated top-k sets
    true_top_k = set([item for item, _ in Counter(true_counts).most_common(k)])
    estimated_top_k = set([item for item, _ in Counter(estimated_counts).most_common(k)])

    intersection = true_top_k & estimated_top_k

    precision = len(intersection) / len(estimated_top_k) if estimated_top_k else 0
    recall = len(intersection) / len(true_top_k) if true_top_k else 0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "precision@k": precision,
        "recall@k": recall,
        "f1@k": f1
    }

def benchmark_all_algos(stream, true_counts, memory_config, top_k=10, prime=False):
    k = memory_config["misra_gries_k"]
    width = memory_config["sketch_width"]
    depth = memory_config["sketch_depth"]

    results = {}

    ### Misra–Gries
    start = time.time()
    mg = MisraGries(k=k)
    for item in stream:
        mg.update(item)
    mg_time = time.time() - start
    mg_est = {item: mg.estimate(item) for item in set(stream)}
    results["MisraGries"] = {
        "runtime": mg_time,
        "errors": compute_errors(mg_est, true_counts),
        "topk": evaluate_top_k(true_counts, mg_est, k=top_k)
    }

    ### Count-Min Sketch
    start = time.time()
    cms = CountMinSketch(width=width, depth=depth, prime=prime)
    for item in stream:
        cms.update(item)
    cms_time = time.time() - start
    cms_est = {item: cms.estimate(item) for item in set(stream)}
    results["CountMinSketch"] = {
        "runtime": cms_time,
        "errors": compute_errors(cms_est, true_counts),
        "topk": evaluate_top_k(true_counts, cms_est, k=top_k),
    }

    ### Count Sketch
    start = time.time()
    cs = BasicCountSketch(width=width, prime=prime)
    for item in stream:
        cs.update(item)
    cs_time = time.time() - start
    cs_est = {item: cs.estimate(item) for item in set(stream)}
    results["CountSketch"] = {
        "runtime": cs_time,
        "errors": compute_errors(cs_est, true_counts),
        "topk": evaluate_top_k(true_counts, cs_est, k=top_k)
    }

    ### Count Median
    start = time.time()
    cm = CountSketchMedian(width=width, depth=depth)
    for item in stream:
        cm.update(item)
    cm_time = time.time() - start
    cm_est = {item: cm.estimate(item) for item in set(stream)}
    results["CountMedian"] = {
        "runtime": cm_time,
        "errors": compute_errors(cm_est, true_counts),
        "topk": evaluate_top_k(true_counts, cm_est, k=top_k)
    }

    return results
