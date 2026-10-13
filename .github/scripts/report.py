"""Build the rebuild-prod timeline report.

Reads the phase timeline and service health collected during the run, prints the timeline to the
job log, writes reports/github-actions/runs/run-<N>.md, appends to the cumulative CSVs and
regenerates reports/github-actions/README.md with every run so far (rebuild and redeploy runs).
"""
import csv
import os
import statistics
from datetime import datetime
from pathlib import Path

MODE_PHASES = {
    "rebuild": [
        "Destroy deployments",
        "Destroy infrastructures",
        "Destroy remote-state",
        "Create remote-state",
        "Create infrastructures",
        "Create deployments",
        "Wait until healthy",
    ],
    "redeploy": [
        "Redeploy deployments",
        "Wait until healthy",
    ],
}
SHORT = {
    "Destroy deployments": "Destroy deploy",
    "Destroy infrastructures": "Destroy infra",
    "Destroy remote-state": "Destroy state",
    "Create remote-state": "Create state",
    "Create infrastructures": "Create infra",
    "Create deployments": "Create deploy",
    "Redeploy deployments": "Redeploy",
    "Wait until healthy": "Healthy",
}

tmp = Path(os.environ["RUNNER_TEMP"])
out = Path("reports/github-actions")
(out / "runs").mkdir(parents=True, exist_ok=True)

mode = os.environ.get("RUN_MODE", "rebuild")
phases = MODE_PHASES[mode]
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


def parse(iso):
    return datetime.fromisoformat(iso)


def hms(iso):
    return parse(iso).strftime("%H:%M:%S") if iso else "–"


timeline = read_rows(tmp / "timeline.csv", ["phase", "start", "end", "seconds", "status"])
services = read_rows(tmp / "services.csv", ["service", "created", "steady", "http"])
by_phase = {r["phase"]: r for r in timeline}

starts = [r["start"] for r in timeline if r["start"]]
ends = [r["end"] for r in timeline if r["end"]]
first = min(starts, key=parse) if starts else ""
last = max(ends, key=parse) if ends else ""
total = (parse(last) - parse(first)).total_seconds() if first and last else None
run_date = parse(first).strftime("%Y-%m-%d %H:%M (UTC%z)") if first else "–"

for s in services:
    try:
        s["seconds"] = round((parse(s["steady"]) - parse(s["created"])).total_seconds())
    except (ValueError, TypeError):
        s["seconds"] = ""

# ---------- per-run report ----------
lines = [
    f"# {mode.capitalize()} prod — run #{run_number}",
    "",
    f"- Mode: **{mode}**",
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
for p in phases:
    r = by_phase.get(p)
    if r:
        lines.append(f"| {p} | {hms(r['start'])} | {hms(r['end'])} | {fmt(r['seconds'])} | {r['status']} |")
    else:
        lines.append(f"| {p} | – | – | – | not run |")
lines.append(f"| **Total** | {hms(first)} | {hms(last)} | **{fmt(total)}** | {job_status} |")

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
        w.writerow(["run_number", "run_id", "mode", "commit", "event", "phase", "start", "end", "seconds", "status"])
    for p in phases:
        r = by_phase.get(p)
        if r:
            w.writerow([run_number, run_id, mode, commit, event, p, r["start"], r["end"], r["seconds"], r["status"]])
    w.writerow([run_number, run_id, mode, commit, event, "Total", first, last,
                round(total) if total is not None else "", job_status])

scsv = out / "service-health.csv"
new = not scsv.exists()
with open(scsv, "a", newline="") as f:
    w = csv.writer(f)
    if new:
        w.writerow(["run_number", "mode", "service", "service_created", "steady_state", "seconds_to_healthy", "http_code"])
    for s in services:
        w.writerow([run_number, mode, s["service"], s["created"], s["steady"], s["seconds"], s["http"]])

# ---------- README with every run, one section per mode ----------
with open(tcsv) as f:
    rows = list(csv.DictReader(f))
runs = {}
for r in rows:
    runs.setdefault(r["run_number"], {"mode": r["mode"], "commit": r["commit"], "phases": {}})["phases"][r["phase"]] = r

md = [
    "# Prod pipeline — GitHub Actions timeline",
    "",
    "Pushing a change to `rebuild.sh` runs a full rebuild (destroy and recreate remote-state → infrastructures → "
    "deployments; ECR repositories and images are kept). Pushing a change to `redeploy.sh` only redeploys the "
    "microservices. This file is regenerated after every run; per-run details are in [`runs/`](runs/), raw data in "
    "`timings.csv` and `service-health.csv`.",
]
for m, m_phases in MODE_PHASES.items():
    m_runs = {n: r for n, r in runs.items() if r["mode"] == m}
    if not m_runs:
        continue
    md += [
        "",
        f"## {m.capitalize()} runs",
        "",
        "| Run | Date | Commit | Result | " + " | ".join(SHORT[p] for p in m_phases) + " | Total |",
        "|---|---|---|---|" + "---|" * len(m_phases) + "---|",
    ]
    for n in sorted(m_runs, key=int):
        ph = m_runs[n]["phases"]
        t = ph.get("Total", {})
        date = parse(t["start"]).strftime("%Y-%m-%d %H:%M") if t.get("start") else "–"
        cells = [fmt(ph[p]["seconds"]) if p in ph else "–" for p in m_phases]
        md.append(f"| [#{n}](runs/run-{int(n):04d}.md) | {date} | `{m_runs[n]['commit']}` | {t.get('status', '–')} | "
                  + " | ".join(cells) + f" | {fmt(t.get('seconds'))} |")

    ok = [r["phases"] for r in m_runs.values() if r["phases"].get("Total", {}).get("status") == "success"]
    if ok:
        md += ["", f"### {m.capitalize()} statistics over {len(ok)} successful run(s)", "",
               "| Phase | Mean | Min | Max | SD |", "|---|---|---|---|---|"]
        for p in m_phases + ["Total"]:
            v = [float(ph[p]["seconds"]) for ph in ok if p in ph and ph[p]["seconds"]]
            if v:
                sd = f"{statistics.stdev(v):.0f}s" if len(v) > 1 else "–"
                md.append(f"| {p} | {fmt(statistics.mean(v))} | {fmt(min(v))} | {fmt(max(v))} | {sd} |")

(out / "README.md").write_text("\n".join(md) + "\n")
