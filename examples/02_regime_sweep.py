import pandas as pd
from mm_sim.params import SimParams, QuoteParams
from mm_sim.simulator import simulate_many

sigmas = [0.01, 0.02, 0.04]
lambda0s = [0.5, 1.0, 2.0]

rows = []
for s in sigmas:
    for l0 in lambda0s:
        sim = SimParams(S0=100.0, sigma=s, T=600, dt=0.1, seed=7)
        quote = QuoteParams(gamma=0.1, k=1.5, lambda0=l0, tick_size=0.01, min_spread_ticks=1)
        summ = simulate_many(sim, quote, n_paths=200)
        rows.append({
            "sigma": s,
            "lambda0": l0,
            "pnl_final_mean": summ["pnl_final"].mean(),
            "pnl_final_std": summ["pnl_final"].std(),
            "max_abs_inventory_mean": summ["max_abs_inventory"].mean(),
            "fills_total_mean": summ["fills_total"].mean(),
        })

out = pd.DataFrame(rows).sort_values(["sigma", "lambda0"])
print(out.to_string(index=False))
