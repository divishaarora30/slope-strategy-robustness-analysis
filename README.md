# Slope Strategy Robustness Analysis

## Overview
This project implements a quantitative trading strategy based on the slope behavior of return series using Lagrangian interpolation. The strategy is backtested on historical data and evaluated across multiple assets (RELINFRA and RPOWER) to assess generalizability and robustness under realistic market conditions.

---

## Strategy Idea
- Computes rolling returns over a fixed window  
- Applies Lagrangian interpolation to estimate local slopes  
- Generates trading signals based on:
  - proportion of positive slopes in the window  
  - direction of the latest slope  

---

## Backtest Results

| Metric     | RELINFRA | RPOWER |
|-----------|----------|--------|
| Return    | (fill)   | (fill) |
| Sharpe    | (fill)   | (fill) |
| Max DD    | (fill)   | (fill) |
| Calmar    | (fill)   | (fill) |

The strategy demonstrates strong performance on RELINFRA but fails to generalize effectively to RPOWER under identical parameter settings, indicating sensitivity to asset-specific dynamics.

---

## Stress Testing

The strategy was evaluated under multiple stress scenarios to assess robustness:

- **Monte Carlo Simulation**  
  Bootstrap resampling of returns to evaluate distribution of outcomes and tail risk  

- **Block Bootstrap**  
  Preserves temporal dependencies and volatility clustering for more realistic simulations  

- **Transaction Cost Analysis**  
  Evaluates the impact of varying trading costs on overall profitability  

- **Slippage & Execution Delay**  
  Simulates real-world execution inefficiencies and latency effects  

---

## Key Insights
- Strategy performs well in trend-persistent assets but lacks cross-asset robustness  
- Performance deteriorates significantly under execution constraints  
- Results are highly sensitive to return path and market structure  
- Transaction costs and slippage materially impact profitability  

---

## How to Run

From the main project folder:

```bash
python src/comparison.py

Tech Stack

Python

NumPy

Pandas