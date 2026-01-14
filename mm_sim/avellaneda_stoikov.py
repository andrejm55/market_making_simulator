from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional, Tuple

from .utils import enforce_spread, floor_to_tick, ceil_to_tick


@dataclass(frozen=True)
class ASState:
    t: float
    T: float
    mid: float
    inventory: int


def avellaneda_stoikov_quotes(
    state: ASState,
    *,
    gamma: float,
    sigma: float,
    k: float,
    tick_size: float,
    min_spread_ticks: int = 1,
    max_spread_ticks: Optional[int] = None,
    inventory_clip: Optional[int] = None,
) -> Tuple[float, float]:
    tau = max(0.0, state.T - state.t)
    q = state.inventory
    if inventory_clip is not None:
        q = int(max(-inventory_clip, min(inventory_clip, q)))

    r = state.mid - q * gamma * (sigma ** 2) * tau

    if gamma <= 0.0:
        raise ValueError("gamma must be > 0")
    if k <= 0.0:
        raise ValueError("k must be > 0")

    h = 0.5 * gamma * (sigma ** 2) * tau + (1.0 / gamma) * math.log(1.0 + (gamma / k))

    bid = r - h
    ask = r + h

    bid = floor_to_tick(bid, tick_size)
    ask = ceil_to_tick(ask, tick_size)

    bid, ask = enforce_spread(bid, ask, state.mid, tick_size, min_spread_ticks, max_spread_ticks)
    return bid, ask
