from __future__ import annotations

import numpy as np
import pandas as pd


def pnl_series(cash: np.ndarray, inv: np.ndarray, mid: np.ndarray) -> np.ndarray:
    return cash + inv * mid


def summarize_path(df: pd.DataFrame) -> dict:
    pnl = df["pnl"].to_numpy()
    ret = np.diff(pnl)
    out = {
        "pnl_final": float(pnl[-1]),
        "pnl_mean_step": float(np.mean(ret)) if ret.size else 0.0,
        "pnl_std_step": float(np.std(ret, ddof=1)) if ret.size > 1 else 0.0,
        "max_abs_inventory": int(np.max(np.abs(df["inventory"].to_numpy()))),
        "fills_total": int(df["fill_bid"].sum() + df["fill_ask"].sum()),
        "fills_bid": int(df["fill_bid"].sum()),
        "fills_ask": int(df["fill_ask"].sum()),
        "spread_mean": float(df["ask"].sub(df["bid"]).mean()),
    }
    out["sharpe_step"] = float(out["pnl_mean_step"] / out["pnl_std_step"]) if out["pnl_std_step"] > 0 else 0.0
    return out
