"""
Re-runs the notebook's own code and checks every number published in the README.
Run from the repo root:  python tests/verify_published_numbers.py
Exits non-zero on any failure. Needs the packages in requirements.txt; Python 3.9+.
"""
import contextlib, io, json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.show = lambda *a, **k: None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
nb = json.load(open("WFM_Demand_Forecasting.ipynb", encoding="utf-8"))
g = {}
for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        with contextlib.redirect_stdout(io.StringIO()):
            exec("".join(cell["source"]), g)
    if "scenarios" in g:
        break          # stop after Module 6; the multichannel section publishes no README figures

np, d, opt, fc = g["np"], g["d"], g["opt"], g["fc"]
sc = g["scenarios"].set_index("Scenario")
lever = lambda prefix: next(v for k, v in sc["vs Baseline"].items() if k.startswith(prefix)) * 100
staffed = d[d["scheduled_actual"] > 0]
wape = np.sum(np.abs(fc["calls"] - fc["forecast"])) / np.sum(fc["calls"]) * 100
sl_before = np.average(staffed["delivered_sl"], weights=staffed["forecast_calls"]) * 100
op = opt[opt["scheduled_actual"] > 0]
sl_after = np.average(op["optimized_sl"], weights=op["forecast_calls"]) * 100

checks = [
    ("Dataset rows = 87,600",                          len(g["raw"]) == 87600),
    ("Holdout WAPE = 21.2%",                           round(wape, 1) == 21.2),
    ("Staffed intervals = 34 (07:00-24:00)",           len(staffed) == 34),
    ("Understaffed 18 of 34 (53%)",                    (staffed["gap"] < 0).sum() == 18),
    ("Overstaffed 15 of 34 (44%)",                     (staffed["gap"] > 0).sum() == 15),
    ("Scheduled 486 vs required 494 FTE-intervals",    staffed["scheduled_actual"].sum() == 486 and staffed["scheduled_fte"].sum() == 494),
    ("Staffed-hours gap within 2% (-1.6%)",            abs(486 / 494 - 1) < 0.02),
    ("Delivered SL = 62.4%",                           round(sl_before, 1) == 62.4),
    ("Redistribution conserves agent-intervals",       opt["optimized_schedule"].sum() == d["scheduled_actual"].sum()),
    ("Redistribution adds none to closed hours",       opt.loc[d["scheduled_actual"] == 0, "optimized_schedule"].sum() == 0),
    ("SL after redistribution = 82.5% (+20.2 pp)",     round(sl_after, 1) == 82.5 and round(sl_after - sl_before, 1) == 20.2),
    ("Lever: +10% headcount = +14.5 pp",               round(lever("Lever 2:"), 1) == 14.5),
    ("Lever: +5 FTE/interval = +33.1 pp",              round(lever("Lever 2b"), 1) == 33.1),
    ("Lever: AHT -15% = +13.8 pp",                     round(lever("Lever 3"), 1) == 13.8),
    ("Lever: shrinkage -4 pts = +6.9 pp",              round(lever("Lever 4"), 1) == 6.9),
    ("Lever: combined = +32.0 pp",                     round(lever("Lever 5"), 1) == 32.0),
]

# Robustness: the same synthetic schedule applied to every weekday profile
plan, sl, T = g["plan"], g["service_level"], g["TOTAL_SHRINKAGE"]
rows = []
for dow in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]:
    x = plan[plan["dow"] == dow].sort_values("interval_30").reset_index(drop=True)
    m = x["interval_30"]
    x["s"] = ((m >= 420) & (m < 960)) * 12 + ((m >= 600) & (m < 1140)) * 8 + ((m >= 900) & (m < 1440)) * 7
    o = x[x["s"] > 0]
    dsl = o.apply(lambda r: 1.0 if r.workload_erlangs <= 0 else
                  sl(r.workload_erlangs, max(1, int(np.floor(r.s * (1 - T)))), 20, 240), axis=1)
    rows.append((dow, (o["s"] < o["scheduled_fte"]).mean(), o["s"].sum() / o["scheduled_fte"].sum() - 1,
                 np.average(dsl, weights=o["forecast_calls"])))
checks += [
    ("All weekdays: 41-53% of intervals understaffed", all(0.40 <= r[1] <= 0.54 for r in rows)),
    ("All weekdays: staffed-hours total within 3%",    all(abs(r[2]) <= 0.031 for r in rows)),
    ("All weekdays: SL 59-67%, below 80% target",      all(0.59 <= r[3] <= 0.67 for r in rows)),
]

fail = 0
for name, ok in checks:
    print(("PASS  " if ok else "FAIL  ") + name); fail += (not ok)
print("\nWeekday robustness (same schedule):")
for dow, u, gap, s in rows:
    print(f"  {dow:<10} understaffed {u:4.0%}  total {gap:+5.1%}  SL {s:5.1%}")
print(f"\n{len(checks) - fail}/{len(checks)} checks passed")
sys.exit(1 if fail else 0)
