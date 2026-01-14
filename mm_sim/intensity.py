from __future__ import annotations

import math


def poisson_fill_prob(lambda_t: float, dt: float) -> float:
    if lambda_t <= 0.0:
        return 0.0
    return 1.0 - math.exp(-lambda_t * dt)


def as_intensity(lambda0: float, k: float, delta: float) -> float:
    if delta < 0.0:
        delta = 0.0
    return lambda0 * math.exp(-k * delta)
