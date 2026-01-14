from mm_sim.params import SimParams, QuoteParams
from mm_sim.simulator import simulate_path

sim = SimParams(S0=100.0, sigma=0.02, T=600, dt=0.1, seed=42)
quote = QuoteParams(gamma=0.1, k=1.5, lambda0=1.0, tick_size=0.01, min_spread_ticks=1)

df = simulate_path(sim, quote)
print(df.tail())
print("Final PnL:", df["pnl"].iloc[-1])
