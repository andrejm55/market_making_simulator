from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class QuoteParams:
    """Parameters for the quoting policy and execution model."""

    gamma: float = 0.1
    k: float = 1.5
    lambda0: float = 1.0
    tick_size: float = 0.01
    min_spread_ticks: int = 1
    max_spread_ticks: Optional[int] = None
    inventory_clip: Optional[int] = None


@dataclass(frozen=True)
class SimParams:
    """Parameters for the midprice process and simulation."""

    S0: float = 100.0
    sigma: float = 0.02
    T: float = 600.0
    dt: float = 0.1
    seed: int = 7
    fee_per_fill: float = 0.0
    max_position: Optional[int] = None


@dataclass(frozen=True)
class Regime:
    """A named regime for sweep comparisons."""

    name: str
    sigma: float
    lambda0: float
