from __future__ import annotations

from dataclasses import asdict
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from .avellaneda_stoikov import ASState, avellaneda_stoikov_quotes
from .intensity import as_intensity, poisson_fill_prob
from .metrics import pnl_series
from .params import QuoteParams, SimParams


def simulate_path(sim: SimParams, quote: QuoteParams) -> pd.DataFrame:
    if sim.dt <= 0:
        raise ValueError("dt must be positive")
    n_steps = int(sim.T / sim.dt)
    rng = np.random.default_rng(sim.seed)

    dW = rng.normal(0.0, np.sqrt(sim.dt), size=n_steps)
    mid = np.empty(n_steps + 1, dtype=float)
    mid[0] = sim.S0
    mid[1:] = sim.S0 + sim.sigma * np.cumsum(dW)

    inventory = np.zeros(n_steps + 1, dtype=int)
    cash = np.zeros(n_steps + 1, dtype=float)
    bid = np.zeros(n_steps + 1, dtype=float)
    ask = np.zeros(n_steps + 1, dtype=float)
    fill_bid = np.zeros(n_steps + 1, dtype=int)
    fill_ask = np.zeros(n_steps + 1, dtype=int)

    for i in range(n_steps):
        t = i * sim.dt
        state = ASState(t=t, T=sim.T, mid=float(mid[i]), inventory=int(inventory[i]))

        b, a = avellaneda_stoikov_quotes(
            state,
            gamma=quote.gamma,
            sigma=sim.sigma,
            k=quote.k,
            tick_size=quote.tick_size,
            min_spread_ticks=quote.min_spread_ticks,
            max_spread_ticks=quote.max_spread_ticks,
            inventory_clip=quote.inventory_clip,
        )
        bid[i] = b
        ask[i] = a

        delta_bid = float(mid[i] - b)
        delta_ask = float(a - mid[i])

        lam_bid = as_intensity(quote.lambda0, quote.k, delta_bid)
        lam_ask = as_intensity(quote.lambda0, quote.k, delta_ask)

        p_bid = poisson_fill_prob(lam_bid, sim.dt)
        p_ask = poisson_fill_prob(lam_ask, sim.dt)

        got_bid = 1 if rng.random() < p_bid else 0
        got_ask = 1 if rng.random() < p_ask else 0

        q = int(inventory[i])
        c = float(cash[i])

        if got_bid:
            if sim.max_position is None or (q + 1) <= sim.max_position:
                q += 1
                c -= b
                c -= sim.fee_per_fill
                fill_bid[i] = 1

        if got_ask:
            if sim.max_position is None or (q - 1) >= -sim.max_position:
                q -= 1
                c += a
                c -= sim.fee_per_fill
                fill_ask[i] = 1

        inventory[i + 1] = q
        cash[i + 1] = c

    bid[-1] = bid[-2]
    ask[-1] = ask[-2]
    pnl = pnl_series(cash, inventory, mid)

    df = pd.DataFrame({
        "t": np.arange(n_steps + 1) * sim.dt,
        "mid": mid,
        "bid": bid,
        "ask": ask,
        "inventory": inventory,
        "cash": cash,
        "pnl": pnl,
        "fill_bid": fill_bid,
        "fill_ask": fill_ask,
    })
    return df


def simulate_many(sim: SimParams, quote: QuoteParams, *, n_paths: int = 100, seed0: Optional[int] = None) -> pd.DataFrame:
    from .metrics import summarize_path

    rows: List[Dict] = []
    base_seed = sim.seed if seed0 is None else int(seed0)

    for j in range(int(n_paths)):
        sim_j = SimParams(**{**asdict(sim), "seed": base_seed + j})
        df = simulate_path(sim_j, quote)
        s = summarize_path(df)
        rows.append({"path": j, **s})

    return pd.DataFrame(rows)
