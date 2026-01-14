# mm_sim

Market making simulator that implements Avellaneda–Stoikov quoting logic with:

- Inventory risk and skew
- Spread control and tick rounding
- Regime comparisons across volatility and order arrival intensity

This is only a simulator, not a production system.

## Quickstart

```bash
pip install -e ".[dev]"
mm-sim --help
```

Run a single simulation:

```bash
mm-sim run --T 600 --dt 0.1 --sigma 0.02 --lambda0 2.0 --k 1.5 --gamma 0.1
```

Run a small regime sweep and save results:

```bash
mm-sim sweep --out results.csv --T 600 --dt 0.1 \
  --sigmas 0.01,0.02,0.04 --lambda0s 0.5,1.0,2.0
```

## Model

### Midprice process
Midprice follows a simple arithmetic Brownian motion:

`S_{t+dt} = S_t + sigma * sqrt(dt) * N(0,1)`

### Fill process
Market order arrivals hitting your bid and ask are Poisson with intensities:

- `lambda_bid = lambda0 * exp(-k * delta_bid)`
- `lambda_ask = lambda0 * exp(-k * delta_ask)`

where `delta_bid = S - bid` and `delta_ask = ask - S`. Per step fill probability is:

`p = 1 - exp(-lambda * dt)`

### Avellaneda–Stoikov quotes
With risk aversion `gamma`, inventory `q`, volatility `sigma`, and time remaining `(T - t)`:

- Reservation price: `r = S - q * gamma * sigma^2 * (T - t)`
- Half spread: `h = (gamma * sigma^2 * (T - t))/2 + (1/gamma) * ln(1 + gamma/k)`
- Quotes: `bid = r - h`, `ask = r + h`

Then we apply tick rounding and optional min/max spread control.

## Project layout

- `mm_sim/` package code
- `tests/` unit tests (basic correctness and invariants)
- `examples/` runnable scripts for experiments


