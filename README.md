# WFM Demand Forecasting Model

**Interval-level intraday call volume forecasting, shrinkage modeling, Erlang C service-level estimation, and FTE gap analysis to support contact-center staffing optimization.**

This project demonstrates an end-to-end Workforce Management (WFM) forecasting and capacity-planning methodology in Python, applied to a real, published call-center arrival dataset. It walks the same planning cycle a WFM analyst runs in a production contact center — from raw interval arrivals through to a staffing gap report and the service level a given schedule would actually deliver.

---

## What it demonstrates

- **Interval-level volume forecasting** — a transparent profile-ratio (percent-of-day) forecast that separates the day-total expectation from the intraday distribution, validated on a holdout and reported with **WAPE** (the volume-weighted error metric WFM teams track), not just MAPE.
- **Workload conversion** — calls × Average Handle Time → offered load (Erlangs).
- **Erlang C service-level modeling** — sizing agents-on-phone to an 80/20 service-level target under a 90% occupancy ceiling, with the queueing assumptions and their real-world caveats stated plainly.
- **Shrinkage modeling** — a fully decomposed shrinkage build-up (breaks, training, coaching, PTO, unproductive time) uplifting the on-phone requirement to scheduled FTEs.
- **Staffing gap analysis** — required vs. a realistic lumpy shift schedule, interval by interval, surfacing over/under-staffed intervals and the delivered service level — demonstrating how total headcount can be right while the intraday distribution is wrong.

## The data

**"Anonymous Bank" call-center dataset** — Service Enterprise Engineering (SEE) Lab, Technion – Israel Institute of Technology (Prof. Avi Mandelbaum); documented by Guedj & Mandelbaum (2000) and widely used in the call-center / queueing literature (Brown et al., 2005).

Accessed via the `Rfssa` package data mirror, which publishes the 1999 arrivals pre-aggregated into **6-minute intervals** (240 intervals/day × 365 days = 87,600 rows):

```
https://github.com/haghbinh/dataset/raw/main/Rfssa_dataset/Callcenter.rds
```

The notebook downloads this file automatically on first run.

## Methodology, not platform

My WFM experience is founder-era (a 350-agent call center, intraday management, service-level/abandonment SLAs, schedule adherence and shrinkage reporting) and predates the modern commercial suites (NICE, Verint, Calabrio). Those tools automate exactly the methodology shown here: interval forecasting, Erlang queueing, shrinkage uplift, and schedule-vs-requirement gap analysis. This project demonstrates that underlying methodology directly in Python — the reasoning that sits beneath any platform.

## Provenance & honesty notes

- The **arrival data is real**; the **WFM overlay is synthetic and labeled as such** throughout the notebook — Average Handle Time (240s), the 34% shrinkage build-up, the 80/20 service-level target, the 90% occupancy ceiling, and the shift schedule are explicit planning assumptions, not values derived from the data.
- **Business logic, WFM domain framing, and operational assumptions are my own**, drawn from contact-center workforce-management experience. AI tooling assisted with Python syntax and plotting code.

## Stack

Python · pandas · NumPy · Matplotlib · Seaborn · `pyreadr` (to read the R `.rds` data) · Jupyter

## Run it

```bash
pip install -r requirements.txt
jupyter notebook WFM_Demand_Forecasting.ipynb
```

Or open the notebook directly — every cell runs top-to-bottom and the dataset is fetched automatically.

## Files

| file | purpose |
|---|---|
| `WFM_Demand_Forecasting.ipynb` | the full analysis, with outputs and charts |
| `requirements.txt` | Python dependencies |
| `README.md` | this file |

## Acknowledgement

Data source: SEE Lab, Technion (Prof. Avi Mandelbaum). The data is free for academic / non-commercial use; please acknowledge the source in any derived work.

## Extensions a production build would add

Abandonment-aware queueing (Erlang A/X), intraday re-forecasting, multi-skill / blended workload, shift-bidding optimization, and a what-if sensitivity layer for AHT and shrinkage.
