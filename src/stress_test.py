import numpy as np


# ---------------------------------------------------
# MONTE CARLO (BOOTSTRAP)
# ---------------------------------------------------
def monte_carlo(bt, num_simulations=1000):

    returns = bt["pnl"].values
    n = len(returns)

    mc_returns = []
    mc_dd = []

    for _ in range(num_simulations):

        sim_returns = np.random.choice(returns, size=n, replace=True)
        equity = np.cumsum(sim_returns)

        total_return = equity[-1]

        running_max = np.maximum.accumulate(equity)
        drawdown = equity - running_max
        max_dd = drawdown.min()

        mc_returns.append(total_return)
        mc_dd.append(max_dd)

    return {
        "avg_return": np.mean(mc_returns),
        "worst_return": np.min(mc_returns),
        "best_return": np.max(mc_returns),
        "avg_dd": np.mean(mc_dd),
        "worst_dd": np.min(mc_dd)
    }


# ---------------------------------------------------
# BLOCK BOOTSTRAP
# ---------------------------------------------------
def block_bootstrap(bt, block_size=5, num_simulations=1000):

    returns = bt["pnl"].values
    n = len(returns)

    blocks = []
    for i in range(n - block_size):
        blocks.append(returns[i:i+block_size])

    blocks = np.array(blocks)

    mc_returns = []
    mc_dd = []

    for _ in range(num_simulations):

        sim = []

        while len(sim) < n:
            block = blocks[np.random.randint(0, len(blocks))]
            sim.extend(block)

        sim = np.array(sim[:n])

        equity = np.cumsum(sim)

        total_return = equity[-1]

        running_max = np.maximum.accumulate(equity)
        drawdown = equity - running_max
        max_dd = drawdown.min()

        mc_returns.append(total_return)
        mc_dd.append(max_dd)

    return {
        "avg_return": np.mean(mc_returns),
        "worst_return": np.min(mc_returns),
        "best_return": np.max(mc_returns),
        "avg_dd": np.mean(mc_dd),
        "worst_dd": np.min(mc_dd)
    }


# ---------------------------------------------------
# TRANSACTION COST TEST
# ---------------------------------------------------
def transaction_cost_test(bt, cost_levels=[0, 0.001, 0.0015, 0.002]):

    returns = bt["pnl"].values
    positions = bt["position"].values
    n = len(returns)

    results = {}

    for cost in cost_levels:

        pnl = []

        for i in range(n):

            ret = returns[i]

            # apply cost when position changes
            if i > 0 and positions[i] != positions[i - 1]:
                ret -= cost

            pnl.append(ret)

        pnl = np.array(pnl)
        equity = np.cumsum(pnl)

        results[cost] = equity[-1]

    return results


# ---------------------------------------------------
# SLIPPAGE + DELAY
# ---------------------------------------------------
def slippage_delay(bt, delay=1, slip_min=0.0002, slip_max=0.001):

    returns = bt["pnl"].values
    positions = bt["position"].values
    n = len(returns)

    adjusted = []

    for i in range(n - delay):

        ret = returns[i + delay]

        if i > 0 and positions[i] != positions[i - 1]:
            slippage = np.random.uniform(slip_min, slip_max)
            ret -= slippage

        adjusted.append(ret)

    adjusted = np.array(adjusted)

    equity = np.cumsum(adjusted)

    total_return = equity[-1]

    running_max = np.maximum.accumulate(equity)
    drawdown = equity - running_max
    max_dd = drawdown.min()

    mean_ret = adjusted.mean()
    std_ret = adjusted.std()

    sharpe = (mean_ret / std_ret) * np.sqrt(252) if std_ret != 0 else 0

    return {
        "return": total_return,
        "sharpe": sharpe,
        "max_dd": max_dd
    }