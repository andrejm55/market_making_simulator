from mm_sim.avellaneda_stoikov import ASState, avellaneda_stoikov_quotes


def test_quotes_bid_less_than_ask():
    st = ASState(t=0.0, T=100.0, mid=100.0, inventory=0)
    bid, ask = avellaneda_stoikov_quotes(
        st, gamma=0.1, sigma=0.02, k=1.5, tick_size=0.01, min_spread_ticks=1
    )
    assert bid < ask
    assert abs((bid / 0.01) - round(bid / 0.01)) < 1e-9
    assert abs((ask / 0.01) - round(ask / 0.01)) < 1e-9


def test_inventory_skew_moves_quotes_down_when_long():
    st0 = ASState(t=0.0, T=100.0, mid=100.0, inventory=0)
    st_long = ASState(t=0.0, T=100.0, mid=100.0, inventory=10)
    b0, a0 = avellaneda_stoikov_quotes(st0, gamma=0.1, sigma=0.02, k=1.5, tick_size=0.01)
    b1, a1 = avellaneda_stoikov_quotes(st_long, gamma=0.1, sigma=0.02, k=1.5, tick_size=0.01)
    assert b1 <= b0
    assert a1 <= a0
