# Frequency Estimation in Data Streams

This project evaluates and compares four key frequency estimation algorithms in streaming data scenarios using limited memory:
- **Misra–Gries**
- **Count-Min Sketch**
- **CountSketch (basic)**
- **Count/Median**

The goal is to understand which algorithm performs best under different distributions, memory constraints, and stream lengths—using both synthetic and real-world data.

---

## Algorithms Compared

| Algorithm      | Error Bound Type  | Norm        | Strengths                 |
|----------------|-------------------|-------------|---------------------------|
| Misra–Gries    | Deterministic      | Top-k       | Best top-k recovery       |
| CountMinSketch | One-sided upper    | L1 norm     | Fast, memory efficient    |
| CountSketch    | Two-sided          | L2 norm     | Unbiased, more variance   |
| Count/Median   | Robust (Median)    | L1 approx.  | Stable, accurate          |

---
## Dataset Used
E-Commerce Sales Dataset
Analyzing and Maximizing Online Business Performance By ANil
https://www.kaggle.com/datasets/thedevastator/unlock-profits-with-e-commerce-sales-data?resource=download 

---
## Key Findings
- Misra–Gries had the best top-k recovery and lowest MAE on uniform and real data.
- Count/Median offered robust accuracy under bursty and skewed distributions.
- CountMinSketch was highly sensitive to memory and prone to overestimation at small sizes.
- CountSketch (basic) underperformed across most tasks due to hash collisions and variance.
- Real-world data reflected bursty/Zipf-like behavior, aligning with synthetic results.
