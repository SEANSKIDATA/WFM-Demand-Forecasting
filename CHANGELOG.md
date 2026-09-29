# Changelog

## 2026-09-24 — Reproducibility audit

Every published number was re-run from the notebook's code. All of them reproduce:
87,600 rows, 21.2% WAPE, 18/34 understaffed (53%), 15/34 overstaffed (44%),
486 vs 494 FTE-intervals, 62.4% service level, 82.5% after redistribution (+20.2 pp).
`tests/verify_published_numbers.py` now checks them (19 checks).

**Fixed**
- **README chart replaced.** `staffing_gap_chart.png` came from an earlier version of the
  analysis (Wednesday 08 Dec 1999: 33% understaffed, 48% overstaffed) that is not in the
  notebook, and contradicted the numbers above it. The notebook now writes this chart itself.
- **Charts showed service level for closed hours.** 00:00–07:00 has no one scheduled, but the
  service-level panels plotted 35–98% there, because the calculation treats zero agents as
  one. Those hours were already excluded from every published figure; the charts now shade
  them as closed.
- **Notebook needed Python 3.12.** Three f-strings used nested quotes. Now runs on 3.9+.
- **Modules 5, 6 and 9 had never been run in the saved notebook,** so the +20.2 pp result
  was not visible on GitHub. All cells now run, with outputs saved.
- **Data file.** The notebook now uses the bundled `Callcenter.rds` instead of downloading.
- **Units.** Service-level changes are reported in percentage points.

**Changed**
- **Module 6 levers.** Added a +10% headcount lever (534 FTE-intervals, +14.5 pp) so
  redistribution is compared with a realistic budget ask. The existing "+5 FTEs" lever is
  kept and labeled as +35% of scheduled hours. The markdown listed a "forecast accuracy"
  lever that the code never ran; it now lists the levers that exist.
- **README framing.** States that the schedule is synthetic and deliberately not
  curve-matched, that the 2% comparison covers staffed hours only, and that the result holds
  across all five weekday profiles. Adds a results table and limitations.

**Not supported by this repository**
- The July 2026 "WFM Decision Lab" infographic (headcount +10% = +8.1, AHT −15% = +5.5,
  shrinkage −5 pts = +4.8, occupancy +2.9, "AHT delivers roughly a quarter" of
  redistribution). No code here produces those values. The notebook gives AHT −15% =
  +13.8 pp, about two-thirds of redistribution, and has no occupancy lever.
