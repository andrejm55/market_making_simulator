import matplotlib.pyplot as plt

def _base_fig(figsize=(12, 5)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.grid(True, alpha=0.3)
    return fig, ax

def plot_mid(df, figsize=(12, 5)):
    fig, ax = _base_fig(figsize)
    ax.plot(df["t"], df["mid"], label="Mid price", color="black", linewidth=1.2)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Price")
    ax.set_title("Mid-price over time")
    ax.legend()
    return fig, ax

def plot_quotes(df, show_mid=True, figsize=(12, 5)):
    fig, ax = _base_fig(figsize)
    if show_mid:
        ax.plot(df["t"], df["mid"], label="Mid", color="black", linewidth=1.0, alpha=0.7)
    ax.plot(df["t"], df["bid"], label="Bid", color="tab:blue", alpha=0.85)
    ax.plot(df["t"], df["ask"], label="Ask", color="tab:orange", alpha=0.85)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Price")
    ax.set_title("Bid and ask quotes over time")
    ax.legend()
    return fig, ax


def plot_inventory(df, max_position=None, figsize=(12, 4)):
    fig, ax = _base_fig(figsize)
    ax.plot(df["t"], df["inventory"], color="tab:green")
    if max_position is not None:
        ax.axhline(max_position, color="red", linestyle="--", alpha=0.6)
        ax.axhline(-max_position, color="red", linestyle="--", alpha=0.6)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Inventory")
    ax.set_title("Inventory over time")
    return fig, ax

def plot_pnl(df, show_components=True, figsize=(12, 5)):
    fig, ax = _base_fig(figsize)
    ax.plot(df["t"], df["pnl"], label="PnL", color="black", linewidth=1.6)
    if show_components:
        ax.plot(df["t"], df["cash"], label="Cash", color="tab:blue", alpha=0.6)
        ax.plot(df["t"], df["inventory"] * df["mid"], label="Inventory value", color="tab:orange", alpha=0.6)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Value")
    ax.set_title("PnL over time")
    ax.legend()
    return fig, ax

def plot_fills_on_price(df, figsize=(12, 5)):
    fig, ax = _base_fig(figsize)
    ax.plot(df["t"], df["mid"], label="Mid", color="black", linewidth=1.0)

    bid_fills = df[df["fill_bid"] == 1]
    ask_fills = df[df["fill_ask"] == 1]

    ax.scatter(bid_fills["t"], bid_fills["mid"], color="green", marker="^", label="Bid fills", s=30)
    ax.scatter(ask_fills["t"], ask_fills["mid"], color="red", marker="v", label="Ask fills", s=30)

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Price")
    ax.set_title("Fill events overlaid on mid-price")
    ax.legend()
    return fig, ax

def plot_bid_ask_step(df, show_mid=True, figsize=(12, 5),downsample=None):
    dfp = df.iloc[::downsample]
    fig, ax = _base_fig(figsize)

    if show_mid:
        ax.step(dfp["t"], dfp["mid"], where="post", label="Mid", color="black", linewidth=1.0, alpha=0.6)

    ax.step(dfp["t"], dfp["bid"], where="post", label="Bid", color="tab:green", linewidth=1.4)
    ax.step(dfp["t"], dfp["ask"], where="post", label="Ask", color="tab:blue", linewidth=1.4)

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Price")
    ax.set_title("Bid-Ask price over time (step plot)")
    ax.legend()
    return fig, ax