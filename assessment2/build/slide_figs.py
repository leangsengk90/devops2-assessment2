"""Chart images for the presentation (slides 9 and 11).

Rendered as PNG rather than native PowerPoint charts so they show the same in
PowerPoint, Keynote and Google Slides. Run after analysis/analyze.py.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
R = json.loads((ROOT / "analysis" / "results.json").read_text())

INK, MUTED, GRID = "#1E1A2B", "#6B6680", "#E4E3DF"
DESTROY, CREATE, MANUAL = "#E39A3B", "#2A78D6", "#EB6834"
plt.rcParams.update({"font.family": "DejaVu Sans", "figure.dpi": 220, "savefig.bbox": "tight",
                     "axes.edgecolor": "#B9B6C6", "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": INK})

P = R["gh_phases"]
N = R["n_tf"]
mins = lambda s: s / 60


def phases():
    rows = [("Destroy 5 service stacks", "Destroy deployments", DESTROY),
            ("Destroy shared infrastructure", "Destroy infrastructures", DESTROY),
            ("Destroy state bucket + lock table", "Destroy remote-state", DESTROY),
            ("Create state bucket + lock table", "Create remote-state", CREATE),
            ("Create shared infrastructure", "Create infrastructures", CREATE),
            ("Create 5 service stacks", "Create deployments", CREATE),
            ("Wait until services healthy", "Wait until healthy", CREATE)]
    fig, ax = plt.subplots(figsize=(6.0, 2.75))
    y = [6.6, 5.6, 4.6, 2.6, 1.6, 0.6, -0.4]  # gap between the destroy and create groups
    xmax = mins(P["Destroy deployments"]["max"]) * 1.3
    for (label, key, col), yy in zip(rows, y):
        p = P[key]
        m, sd = mins(p["mean"]), mins(p["sd"])
        ax.barh(yy, m, height=0.68, color=col, zorder=2)
        ax.plot([mins(p["min"]), mins(p["max"])], [yy, yy], color=INK, lw=0.9, zorder=3)
        for v in (p["min"], p["max"]):
            ax.plot([mins(v)] * 2, [yy - 0.13, yy + 0.13], color=INK, lw=0.9, zorder=3)
        ax.text(mins(p["max"]) + xmax * 0.012, yy, f"{m:.1f} min · SD {p['sd']:.0f} s",
                va="center", fontsize=9.5, color=INK)
    ax.set_yticks(y, [r[0] for r in rows], fontsize=10)
    ax.set_xlim(0, xmax)
    ax.set_ylim(-1.0, 7.9)
    ax.set_xlabel("Minutes · bar = mean of 30 runs · line = fastest to slowest run", fontsize=9)
    ax.tick_params(axis="x", labelsize=8)
    ax.grid(axis="x", color=GRID, lw=0.6, zorder=0)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fd, fc = P["Full destroy"], P["Full create"]
    tot = P["Total cycle"]["mean"]
    ax.text(0, 7.45, f"DESTROY  {mins(fd['mean']):.1f} min  ·  {fd['mean'] / tot * 100:.0f}% of the cycle",
            fontsize=10.5, fontweight="bold", color=DESTROY, va="center")
    ax.text(0, 3.45, f"CREATE  {mins(fc['mean']):.1f} min  ·  {fc['mean'] / tot * 100:.0f}% of the cycle",
            fontsize=10.5, fontweight="bold", color=CREATE, va="center")
    fig.savefig(FIG / "slide_phases.png")
    plt.close(fig)


def h1():
    tf, man = P["Full create"], R["sim_manual"]
    fig, ax = plt.subplots(figsize=(4.6, 3.1))
    labels = [f"Terraform via\nGitHub Actions\n(measured, n = {N})", f"Manual AWS console\n(SIMULATED, n = {man['n']})"]
    vals = [mins(tf["mean"]), mins(man["mean"])]
    lo = [vals[0] - mins(tf["ci_low"]), vals[1] - mins(man["ci_low"])]
    hi = [mins(tf["ci_high"]) - vals[0], mins(man["ci_high"]) - vals[1]]
    bars = ax.bar([0, 1], vals, width=0.55, color=[CREATE, MANUAL], zorder=2,
                  yerr=[lo, hi], capsize=5, error_kw={"lw": 1, "ecolor": INK})
    bars[1].set_hatch("///")
    bars[1].set_edgecolor("white")
    for x, v, h in zip([0, 1], vals, hi):
        ax.text(x, v + h + 2.5, f"{v:.1f} min", ha="center", fontsize=11, fontweight="bold", color=INK)
    ax.annotate(f"{R['h1']['ratio']:.1f}× faster", xy=(0.3, vals[0] + 6), xytext=(0.5, vals[1] * 0.55),
                ha="center", fontsize=10.5, fontweight="bold", color=INK,
                arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 1})
    ax.set_xticks([0, 1], labels, fontsize=8.5)
    ax.set_ylabel("Minutes to build from empty (mean, 95% CI)", fontsize=8.5)
    ax.set_ylim(0, vals[1] * 1.22)
    ax.tick_params(axis="y", labelsize=8, colors=MUTED)
    ax.grid(axis="y", color=GRID, lw=0.6, zorder=0)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.savefig(FIG / "slide_h1.png")
    plt.close(fig)


if __name__ == "__main__":
    phases()
    h1()
    print("saved slide_phases.png, slide_h1.png")
