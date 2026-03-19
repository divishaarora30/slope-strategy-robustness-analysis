import pandas as pd
import numpy as np


# -----------------------------
# PARAMETERS
# -----------------------------
canddow = 6
lol = 0.5


# -----------------------------
# SLOPE FUNCTION (LAGRANGE)
# -----------------------------
def slopemech(returns):

    n = len(returns)
    x = np.arange(n)
    slopes = np.zeros(n)

    for point in range(n):

        slope_value = 0

        for i in range(n):

            inner_sum = 0

            for k in range(n):

                if k != i:

                    product_term = 1

                    for j in range(n):

                        if j != i and j != k:
                            product_term *= (x[point] - x[j]) / (x[i] - x[j])

                    inner_sum += product_term / (x[i] - x[k])

            slope_value += returns[i] * inner_sum

        slopes[point] = slope_value

    return slopes


# -----------------------------
# MAIN BACKTEST FUNCTION
# -----------------------------
def run_backtest(file_path, stock_name):

    # Load data
    stock = pd.read_csv(file_path)

    if "Date" in stock.columns:
        stock = stock.rename(columns={"Date": "Timestamp"})

    if "Adj Close" in stock.columns:
        stock = stock.rename(columns={"Adj Close": "Close"})

    stock["Timestamp"] = pd.to_datetime(stock["Timestamp"])
    stock = stock.sort_values("Timestamp").reset_index(drop=True)

    stock = stock[["Timestamp", "Close"]]

    print(f"\nRunning backtest for {stock_name}")
    print("Rows loaded:", len(stock))

    # Returns
    stock["ret"] = stock["Close"].pct_change()

    # Backtest
    positions = []
    pnl = []
    currposition = 0

    for i in range(canddow, len(stock) - 1):

        windowreturns = stock["ret"].iloc[i - canddow:i].values

        position = currposition
        tradereturn = 0

        if not np.isnan(windowreturns).any():

            slopes = slopemech(windowreturns)

            posslopes = (slopes > 0).sum()
            ratio = posslopes / canddow
            latslope = slopes[-1]

            signal = (ratio >= lol) and (latslope > 0)

            if currposition == 0 and signal:
                position = 1

            elif currposition == 1 and not signal:
                position = 0

        if currposition == 1:
            tradereturn = stock["ret"].iloc[i + 1]

        positions.append(position)
        pnl.append(tradereturn)

        currposition = position

    # Results dataframe
    bt = stock.iloc[canddow:len(stock) - 1].copy()
    bt["position"] = positions
    bt["pnl"] = pnl
    bt["equity"] = bt["pnl"].cumsum()

    # Metrics
    total_return = bt["equity"].iloc[-1]

    dailyreturns = bt["pnl"]
    mean_ret = dailyreturns.mean()
    std_ret = dailyreturns.std()

    sharpe = (mean_ret / std_ret) * np.sqrt(252) if std_ret != 0 else 0

    equity = bt["equity"]
    rollingmax = equity.cummax()
    drawdown = equity - rollingmax
    max_dd = drawdown.min()

    trades = (bt["position"].diff() == 1).sum()
    winrate = (bt["pnl"] > 0).sum() / trades if trades > 0 else 0

    calmar = (mean_ret * 252) / abs(max_dd) if max_dd != 0 else 0

    # Print results
    print("\nRESULTS:")
    print("Total Return :", round(total_return, 4))
    print("Sharpe Ratio :", round(sharpe, 2))
    print("Max Drawdown :", round(max_dd, 4))
    print("Win Rate     :", f"{winrate:.2%}")
    print("Calmar Ratio :", round(calmar, 2))

    return {
        "stock": stock_name,
        "return": total_return,
        "sharpe": sharpe,
        "max_dd": max_dd,
        "winrate": winrate,
        "calmar": calmar,
        "bt": bt
    }


# -----------------------------
# RUN FOR BOTH STOCKS
# -----------------------------
if __name__ == "__main__":

    relinfra = run_backtest("data/RELINFRA_2022_2025.csv", "RELINFRA")
    rpower   = run_backtest("data/RPOWER_2022_2025.csv", "RPOWER")