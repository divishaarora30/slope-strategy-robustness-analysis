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

| Metric    | RELINFRA | RPOWER  |
|-----------|----------|---------|
| Return    | 166.34%  | 62.87%  |
| Sharpe    | 1.41     | 0.57    |
| Max DD    | -30.87%  | -59.72% |
| Calmar    | 1.86     | 0.36    |

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

1. Download or clone this repository.

2. Open a terminal inside the project folder.

3. Run the following command:

python src/comparison.py
