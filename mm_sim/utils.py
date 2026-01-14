from __future__ import annotations

import math
from typing import Optional, Tuple


def round_to_tick(x: float, tick: float) -> float:
    return round(x / tick) * tick


def floor_to_tick(x: float, tick: float) -> float:
    return math.floor(x / tick) * tick


def ceil_to_tick(x: float, tick: float) -> float:
    return math.ceil(x / tick) * tick


def enforce_spread(
    bid: float,
    ask: float,
    mid: float,
    tick: float,
    min_spread_ticks: int,
    max_spread_ticks: Optional[int],
) -> Tuple[float, float]:
    if ask <= bid:
        bid = floor_to_tick(mid - tick, tick)
        ask = ceil_to_tick(mid + tick, tick)

    spread_ticks = int(round((ask - bid) / tick))
    min_ticks = max(1, int(min_spread_ticks))
    if spread_ticks < min_ticks:
        half = (min_ticks * tick) / 2.0
        bid = floor_to_tick(mid - half, tick)
        ask = ceil_to_tick(mid + half, tick)

    if max_spread_ticks is not None:
        max_ticks = int(max_spread_ticks)
        spread_ticks = int(round((ask - bid) / tick))
        if spread_ticks > max_ticks:
            half = (max_ticks * tick) / 2.0
            bid = floor_to_tick(mid - half, tick)
            ask = ceil_to_tick(mid + half, tick)

    bid = floor_to_tick(bid, tick)
    ask = ceil_to_tick(ask, tick)
    if ask <= bid:
        ask = bid + tick
    return bid, ask
