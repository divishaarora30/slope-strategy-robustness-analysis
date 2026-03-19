from backtest import run_backtest
from stress_test import monte_carlo, block_bootstrap, transaction_cost_test, slippage_delay

print("\nRUNNING CROSS-ASSET COMPARISON...\n")


# -----------------------------
# RUN BACKTEST FOR BOTH STOCKS
# -----------------------------
relinfra = run_backtest("data/RELINFRA_2022_2025.csv", "RELINFRA")
rpower   = run_backtest("data/RPOWER_2022_2025.csv", "RPOWER")


# -----------------------------
# PRINT COMPARISON TABLE
# -----------------------------
print("\n==============================")
print("   COMPARATIVE ANALYSIS")
print("==============================\n")

print(f"{'Metric':<15}{'RELINFRA':<15}{'RPOWER':<15}")
print("-" * 45)

print(f"{'Return':<15}{relinfra['return']:<15.4f}{rpower['return']:<15.4f}")
print(f"{'Sharpe':<15}{relinfra['sharpe']:<15.2f}{rpower['sharpe']:<15.2f}")
print(f"{'Max DD':<15}{relinfra['max_dd']:<15.4f}{rpower['max_dd']:<15.4f}")
print(f"{'Win Rate':<15}{relinfra['winrate']:<15.2%}{rpower['winrate']:<15.2%}")
print(f"{'Calmar':<15}{relinfra['calmar']:<15.2f}{rpower['calmar']:<15.2f}")

# -----------------------------
# STRESS TESTING
# -----------------------------
print("\n==============================")
print("   STRESS TESTING RESULTS")
print("==============================")


for stock_name, result in [("RELINFRA", relinfra), ("RPOWER", rpower)]:

    bt = result["bt"]

    print(f"\n====== {stock_name} ======")

    # Monte Carlo
    mc = monte_carlo(bt)
    print("\nMonte Carlo:")
    print(f"Avg Return : {mc['avg_return']:.4f}")
    print(f"Worst Ret  : {mc['worst_return']:.4f}")
    print(f"Worst DD   : {mc['worst_dd']:.4f}")

    # Block Bootstrap
    bb = block_bootstrap(bt)
    print("\nBlock Bootstrap:")
    print(f"Avg Return : {bb['avg_return']:.4f}")
    print(f"Worst Ret  : {bb['worst_return']:.4f}")
    print(f"Worst DD   : {bb['worst_dd']:.4f}")

    # Transaction Cost
    tc = transaction_cost_test(bt)
    print("\nTransaction Cost Impact:")
    for cost, ret in tc.items():
        print(f"Cost {cost*100:.2f}% → Return {ret:.4f}")

    # Slippage + Delay
    sd = slippage_delay(bt)
    print("\nSlippage + Delay:")
    print(f"Return : {sd['return']:.4f}")
    print(f"Sharpe : {sd['sharpe']:.2f}")
    print(f"Max DD : {sd['max_dd']:.4f}")


print("\n==============================\n")