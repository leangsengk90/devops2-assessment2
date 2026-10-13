"""Build the rebuild-prod timeline report.

Reads the phase timeline and service health collected during the run, prints the timeline to the
job log, writes reports/github-actions/runs/run-<N>.md, appends to the cumulative CSVs and
regenerates reports/github-actions/README.md with every run so far.
"""
import csv
import os
import statistics
from datetime import datetime
from pathlib import Path

PHASES = [
    "Destroy deployments",
    "Destroy infrastructures",
    "Destroy remote-state",
    "Create remote-state",
    "Create infrastructures",
    "Create deployments",
    "Wait until healthy",
]

tmp = Path(os.environ["RUNNER_TEMP"])
out = Path("reports/github-actions")
(out / "runs").mkdir(parents=True, exist_ok=True)

run_number = os.environ["GITHUB_RUN_NUMBER"]
run_id = os.environ["GITHUB_RUN_ID"]
commit = os.environ["GITHUB_SHA"][:7]
event = os.environ["GITHUB_EVENT_NAME"]
job_status = os.environ.get("JOB_STATUS", "unknown")
api = os.environ.get("API_ENDPOINT", "")
run_url = f"{os.environ['GITHUB_SERVER_URL']}/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{run_id}"


def read_rows(path, fields):
    if not path.exists():
        return []
    with open(path) as f:
        return [dict(zip(fields, line)) for line in csv.reader(f) if line]


def fmt(seconds):
    if seconds in ("", None):
        return "–"
    m, s = divmod(int(round(float(seconds))), 60)
    return f"{m}m {s:02d}s" if m else f"{s}s"


def hms(iso):
    return datetime.fromisoformat(iso).strftime("%H:%M:%S") if iso else "–"


timeline = read_rows(tmp / "timeline.csv", ["phase", "start", "end", "seconds", "status"])
services = read_rows(tmp / "services.csv", ["service", "created", "steady", "http"])
by_phase = {r["phase"]: r for r in timeline}

starts = [r["start"] for r in timeline if r["start"]]
ends = [r["end"] for r in timeline if r["end"]]
total = (
    (datetime.fromisoformat(max(ends)) - datetime.fromisoformat(min(starts))).total_seconds()
    if starts and ends
    else None
)
run_date = datetime.fromisoformat(min(starts)).strftime("%Y-%m-%d %H:%M %Z") if starts else "–"

for s in services:
    if s["created"] and s["steady"] and s["steady"] != "None":
        s["seconds"] = round(
            (datetime.fromisoformat(s["steady"]) - datetime.fromisoformat(s["created"])).total_seconds()
        )
    else:
        s["seconds"] = ""

# ---------- per-run report ----------
lines = [
    f"# Rebuild prod — run #{run_number}",
    "",
    f"- Date: {run_date}",
    f"- Commit: `{commit}` ({event})",
    f"- Result: **{job_status}**",
    f"- Total: **{fmt(total)}**",
    f"- Run: {run_url}",
    "",
    "## Timeline",
    "",
    "| Phase | Start | End | Duration | Status |",
    "|---|---|---|---|---|",
]
for p in PHASES:
    r = by_phase.get(p)
    if r:
        lines.append(f"| {p} | {hms(r['start'])} | {hms(r['end'])} | {fmt(r['seconds'])} | {r['status']} |")
    else:
        lines.append(f"| {p} | – | – | – | not run |")
lines.append(f"| **Total** | {hms(min(starts)) if starts else '–'} | {hms(max(ends)) if ends else '–'} | **{fmt(total)}** | {job_status} |")

if services:
    lines += ["", "## Services", "", "| Service | URL | Time to healthy | HTTP |", "|---|---|---|---|"]
    for s in services:
        url = f"{api}/{s['service']}" if api else "–"
        lines.append(f"| {s['service']} | {url} | {fmt(s['seconds'])} | {s['http']} |")

report = "\n".join(lines) + "\n"
(out / "runs" / f"run-{int(run_number):04d}.md").write_text(report)
print(report)

summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
if summary_file:
    with open(summary_file, "a") as f:
        f.write(report)

# ---------- cumulative CSVs ----------
tcsv = out / "timings.csv"
new = not tcsv.exists()
with open(tcsv, "a", newline="") as f:
    w = csv.writer(f)
    if new:
        w.writerow(["run_number", "run_id", "commit", "event", "phase", "start", "end", "seconds", "status"])
    for p in PHASES:
        r = by_phase.get(p)
        if r:
            w.writerow([run_number, run_id, commit, event, p, r["start"], r["end"], r["seconds"], r["status"]])
    w.writerow([run_number, run_id, commit, event, "Total", min(starts) if starts else "", max(ends) if ends else "",
                round(total) if total is not None else "", job_status])

scsv = out / "service-health.csv"
new = not scsv.exists()
with open(scsv, "a", newline="") as f:
    w = csv.writer(f)
    if new:
        w.writerow(["run_number", "service", "service_created", "steady_state", "seconds_to_healthy", "http_code"])
    for s in services:
        w.writerow([run_number, s["service"], s["created"], s["steady"], s["seconds"], s["http"]])

# ---------- README with every run ----------
with open(tcsv) as f:
    rows = list(csv.DictReader(f))
runs = {}
for r in rows:
    runs.setdefault(r["run_number"], {})[r["phase"]] = r

short = ["Destroy deploy", "Destroy infra", "Destroy state", "Create state", "Create infra", "Create deploy", "Healthy"]
md = [
    "# Rebuild prod — GitHub Actions timeline",
    "",
    "Each push to `main` destroys and recreates remote-state → infrastructures → deployments "
    "(ECR repositories and images are kept). This file is regenerated after every run; "
    "per-run details are in [`runs/`](runs/), raw data in `timings.csv` and `service-health.csv`.",
    "",
    "| Run | Date | Commit | Result | " + " | ".join(short) + " | Total |",
    "|---|---|---|---|" + "---|" * len(short) + "---|",
]
for n in sorted(runs, key=int):
    ph = runs[n]
    t = ph.get("Total", {})
    date = datetime.fromisoformat(t["start"]).strftime("%Y-%m-%d %H:%M") if t.get("start") else "–"
    any_row = next(iter(ph.values()))
    cells = [fmt(ph[p]["seconds"]) if p in ph else "–" for p in PHASES]
    md.append(f"| [#{n}](runs/run-{int(n):04d}.md) | {date} | `{any_row['commit']}` | {t.get('status', '–')} | "
              + " | ".join(cells) + f" | {fmt(t.get('seconds'))} |")

ok = [ph for ph in runs.values() if ph.get("Total", {}).get("status") == "success"]
if len(ok) >= 1:
    def col(p):
        vals = [float(ph[p]["seconds"]) for ph in ok if p in ph and ph[p]["seconds"]]
        return vals
    md += ["", f"## Statistics over {len(ok)} successful run(s)", "", "| Phase | Mean | Min | Max | SD |", "|---|---|---|---|---|"]
    for p in PHASES + ["Total"]:
        v = col(p)
        if v:
            sd = f"{statistics.stdev(v):.0f}s" if len(v) > 1 else "–"
            md.append(f"| {p} | {fmt(statistics.mean(v))} | {fmt(min(v))} | {fmt(max(v))} | {sd} |")

(out / "README.md").write_text("\n".join(md) + "\n")
