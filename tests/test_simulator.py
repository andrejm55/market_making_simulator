from mm_sim.params import SimParams, QuoteParams
from mm_sim.simulator import simulate_path


def test_simulation_outputs_columns():
    sim = SimParams(S0=100.0, sigma=0.02, T=10.0, dt=0.1, seed=1)
    quote = QuoteParams(gamma=0.1, k=1.5, lambda0=1.0, tick_size=0.01)
    df = simulate_path(sim, quote)
    for col in ["t","mid","bid","ask","inventory","cash","pnl","fill_bid","fill_ask"]:
        assert col in df.columns
    assert len(df) == int(sim.T / sim.dt) + 1


def test_position_limit_respected():
    sim = SimParams(S0=100.0, sigma=0.02, T=10.0, dt=0.1, seed=2, max_position=1)
    quote = QuoteParams(gamma=0.1, k=1.5, lambda0=50.0, tick_size=0.01)
    df = simulate_path(sim, quote)
    assert df["inventory"].abs().max() <= 1
