"""Diagrams for Chapters 2, 3 and 5 (Figures 2.1, 3.1, 5.1)."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

FIG = Path(__file__).resolve().parent.parent / "figures"
NAVY, INK, MUTED = "#1F3864", "#0b0b0b", "#52514e"
F_IV, F_MOD, F_DV, F_CTL, F_QUAL, F_INT = "#dfe9f6", "#fff1cc", "#ffffff", "#f1f1ef", "#fff1cc", "#e2efda"
plt.rcParams.update({"font.family": "DejaVu Sans", "figure.dpi": 200, "savefig.bbox": "tight"})


def box(ax, x, y, w, h, text, fill, bold=False, fs=9, ls="-", ec=NAVY):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.08",
                                fc=fill, ec=ec, lw=1.4, ls=ls))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=INK,
            fontweight="bold" if bold else "normal", linespacing=1.35)


def arrow(ax, a, b, ls="-", color=NAVY, lw=1.6, label=None, lpos=0.5, loff=(0, 0.12), rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=13, lw=lw, color=color,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))
    if label:
        x = a[0] + (b[0] - a[0]) * lpos + loff[0]
        y = a[1] + (b[1] - a[1]) * lpos + loff[1]
        ax.text(x, y, label, fontsize=9, color=NAVY, fontweight="bold", ha="center", va="center",
                bbox=dict(fc="white", ec="none", pad=0.6))


def framework(name, statuses=None):
    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    box(ax, 0.1, 2.35, 2.6, 1.5, "Provisioning method\n(independent variable)\n\nTerraform via GitHub Actions\nvs. manual AWS console", F_IV, fs=8.5)
    box(ax, 3.55, 4.85, 2.9, 0.95, "Pipeline integration depth\n(moderator)", F_MOD, fs=8.5)
    dv = [("Provisioning duration (DV1)", 4.45), ("Configuration drift (DV2)", 3.35),
          ("Reproducibility (DV3)", 2.25), ("Version-control coverage (DV4)", 1.15)]
    ys = {}
    for i, (t, y) in enumerate(dv):
        s = statuses[i] if statuses else None
        lbl = t if not s else f"{t}\n{s[0]}"
        box(ax, 7.0, y - 0.38, 2.9, 0.76, lbl, F_DV, fs=8.3, ls="--" if s and s[1] == "untested" else "-",
            ec=MUTED if s and s[1] == "untested" else NAVY)
        ys[i] = y
    for i, (h, y) in enumerate(zip(["H1", "H2", "H3", "H4"], ys.values())):
        untested = statuses and statuses[i][1] == "untested"
        arrow(ax, (2.72, 3.1), (6.98, y), ls=(0, (4, 3)) if untested else "-",
              color=MUTED if untested else NAVY, label=h, lpos=0.42, loff=(0, 0.13))
    # H5: moderator acts on the method -> drift path (H2)
    mx, my = 2.72 + (6.98 - 2.72) * 0.62, 3.1 + (3.35 - 3.1) * 0.62
    unt5 = statuses and statuses[4][1] == "untested"
    arrow(ax, (5.0, 4.83), (mx, my + 0.03), ls=(0, (5, 3)), color=MUTED if unt5 else NAVY)
    ax.text(5.25, 4.55, "H5" + (f"\n{statuses[4][0]}" if statuses else ""), fontsize=9 if not statuses else 7.8,
            color=NAVY, fontweight="bold", ha="left", va="center")
    box(ax, 3.55, 0.1, 2.9, 0.85, "Control variables\nAWS region · account · time · run order", F_CTL, fs=8, ec=MUTED)
    arrow(ax, (6.47, 0.55), (6.98, 1.0), ls=":", color=MUTED, lw=1.2)
    fig.savefig(FIG / name)
    plt.close(fig)


def design():
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.6)
    ax.axis("off")
    ax.text(0.1, 5.35, "PHASE 1   QUANTITATIVE  (dominant strand)", fontsize=11, color=NAVY, fontweight="bold")
    box(ax, 0.1, 3.75, 2.95, 1.2, "QUAN data collection\n30 GitHub Actions rebuilds\n10 SIMULATED manual builds\ncoverage audit", F_IV, fs=8)
    box(ax, 3.55, 3.75, 2.95, 1.2, "QUAN analysis\ndescriptives, Shapiro–Wilk,\nWelch t, Mann–Whitney U,\nHedges g, Fisher exact", F_IV, fs=8)
    box(ax, 7.0, 3.75, 2.9, 1.2, "Results requiring\nexplanation identified", F_IV, fs=8.5)
    arrow(ax, (3.07, 4.35), (3.53, 4.35))
    arrow(ax, (6.52, 4.35), (6.98, 4.35))
    arrow(ax, (8.45, 3.73), (8.45, 2.75))
    ax.text(8.6, 3.2, "case selection", fontsize=8.5, color=MUTED, style="italic")
    ax.text(0.1, 2.95, "PHASE 2   qualitative  (supporting strand)", fontsize=11, color=NAVY, fontweight="bold")
    box(ax, 7.0, 1.55, 2.9, 1.15, "qual data collection\n78 commits, 31 run reports,\npipeline code and logs", F_QUAL, fs=8)
    box(ax, 3.55, 1.55, 2.95, 1.15, "qual analysis\nreflexive thematic\nanalysis", F_QUAL, fs=8.5)
    arrow(ax, (6.98, 2.12), (6.52, 2.12))
    box(ax, 3.55, 0.05, 2.95, 1.1, "PHASE 3   Integration\njoint display\nmeta-inference", F_INT, bold=True, fs=8.5)
    arrow(ax, (5.02, 1.53), (5.02, 1.17))
    fig.savefig(FIG / "fig3_1_design.png")
    plt.close(fig)


if __name__ == "__main__":
    framework("fig2_1_framework.png")
    framework("fig5_1_revised_framework.png", statuses=[
        ("supported vs. simulated manual", "ok"), ("not tested: one environment", "untested"),
        ("30/30 vs. 3/10 simulated manual", "ok"), ("79% fully codified", "ok"),
        ("not tested", "untested")])
    design()
    print("ok")
