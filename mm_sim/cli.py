from __future__ import annotations

import argparse
from dataclasses import asdict

import pandas as pd

from .params import QuoteParams, SimParams
from .simulator import simulate_many, simulate_path


def _csv_list(x: str) -> list[float]:
    return [float(s.strip()) for s in x.split(",") if s.strip()]


def cmd_run(args: argparse.Namespace) -> int:
    sim = SimParams(
        S0=args.S0,
        sigma=args.sigma,
        T=args.T,
        dt=args.dt,
        seed=args.seed,
        fee_per_fill=args.fee,
        max_position=args.max_position,
    )
    quote = QuoteParams(
        gamma=args.gamma,
        k=args.k,
        lambda0=args.lambda0,
        tick_size=args.tick,
        min_spread_ticks=args.min_spread_ticks,
        max_spread_ticks=args.max_spread_ticks,
        inventory_clip=args.inventory_clip,
    )

    df = simulate_path(sim, quote)
    if args.out:
        df.to_csv(args.out, index=False)
    else:
        print(df.tail(10).to_string(index=False))
    print()
    print("Final PnL:", float(df["pnl"].iloc[-1]))
    print("Final inventory:", int(df["inventory"].iloc[-1]))
    return 0


def cmd_sweep(args: argparse.Namespace) -> int:
    sigmas = _csv_list(args.sigmas)
    lambda0s = _csv_list(args.lambda0s)

    quote_base = QuoteParams(
        gamma=args.gamma,
        k=args.k,
        lambda0=1.0,
        tick_size=args.tick,
        min_spread_ticks=args.min_spread_ticks,
        max_spread_ticks=args.max_spread_ticks,
        inventory_clip=args.inventory_clip,
    )

    rows = []
    for s in sigmas:
        for l0 in lambda0s:
            sim = SimParams(
                S0=args.S0,
                sigma=s,
                T=args.T,
                dt=args.dt,
                seed=args.seed,
                fee_per_fill=args.fee,
                max_position=args.max_position,
            )
            quote = QuoteParams(**{**asdict(quote_base), "lambda0": l0})
            summ = simulate_many(sim, quote, n_paths=args.n_paths)
            agg = summ.mean(numeric_only=True).to_dict()
            agg_std = summ.std(numeric_only=True).to_dict()
            rows.append({
                "sigma": s,
                "lambda0": l0,
                "n_paths": args.n_paths,
                **{f"{k}_mean": float(v) for k, v in agg.items()},
                **{f"{k}_std": float(v) for k, v in agg_std.items()},
            })

    out = pd.DataFrame(rows).sort_values(["sigma", "lambda0"])
    if args.out:
        out.to_csv(args.out, index=False)
    else:
        print(out.to_string(index=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="mm-sim", description="Basic market making simulator with Avellaneda–Stoikov quoting.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_common(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("--S0", type=float, default=100.0)
        sp.add_argument("--T", type=float, default=600.0)
        sp.add_argument("--dt", type=float, default=0.1)
        sp.add_argument("--seed", type=int, default=7)
        sp.add_argument("--fee", type=float, default=0.0)
        sp.add_argument("--max-position", type=int, default=None)

        sp.add_argument("--gamma", type=float, default=0.1)
        sp.add_argument("--k", type=float, default=1.5)
        sp.add_argument("--tick", type=float, default=0.01)
        sp.add_argument("--min-spread-ticks", type=int, default=1)
        sp.add_argument("--max-spread-ticks", type=int, default=None)
        sp.add_argument("--inventory-clip", type=int, default=None)

    sp_run = sub.add_parser("run", help="Run one simulation path.")
    add_common(sp_run)
    sp_run.add_argument("--sigma", type=float, default=0.02)
    sp_run.add_argument("--lambda0", type=float, default=1.0)
    sp_run.add_argument("--out", type=str, default=None, help="Optional CSV output path.")
    sp_run.set_defaults(func=cmd_run)

    sp_sw = sub.add_parser("sweep", help="Sweep regimes over sigma and lambda0.")
    add_common(sp_sw)
    sp_sw.add_argument("--sigmas", type=str, default="0.01,0.02,0.04")
    sp_sw.add_argument("--lambda0s", type=str, default="0.5,1.0,2.0")
    sp_sw.add_argument("--n-paths", type=int, default=100)
    sp_sw.add_argument("--out", type=str, default="results.csv")
    sp_sw.set_defaults(func=cmd_sweep)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
