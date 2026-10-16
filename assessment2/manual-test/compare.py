#!/usr/bin/env python3
"""Compare two exports and count how far a build differs from the baseline.

Usage:  python3 compare.py exports/terraform-baseline.json exports/manual-run-1.json

Prints every difference and a summary, and appends one row to comparisons.csv:
  missing   = resources in the baseline but not in the build
  extra     = resources in the build but not in the baseline
  config    = settings that differ on resources present in both (tags excluded)
  tags      = tag differences (reported separately so they don't hide configuration errors)
A build is "identical" when missing = extra = config = 0.
"""
import csv
import json
import sys
from pathlib import Path


def flatten(o, prefix=""):
    out = {}
    if isinstance(o, dict):
        for k, v in o.items():
            out.update(flatten(v, f"{prefix}.{k}" if prefix else k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out.update(flatten(v, f"{prefix}[{i}]"))
    else:
        out[prefix] = o
    return out


def is_tag(path):
    p = path.lower()
    return p.startswith("tags") or ".tags" in p or "tagset" in p


def main(base_path, build_path):
    base = json.loads(Path(base_path).read_text())
    build = json.loads(Path(build_path).read_text())
    A, B = base["resources"], build["resources"]
    missing = sorted(set(A) - set(B))
    extra = sorted(set(B) - set(A))
    config, tags = [], []
    for key in sorted(set(A) & set(B)):
        fa, fb = flatten(A[key]), flatten(B[key])
        for path in sorted(set(fa) | set(fb)):
            va, vb = fa.get(path, "<absent>"), fb.get(path, "<absent>")
            if va != vb:
                (tags if is_tag(path) else config).append((key, path, va, vb))

    print(f"Baseline: {base['label']} ({len(A)} resources)   Build: {build['label']} ({len(B)} resources)\n")
    for k in missing:
        print(f"MISSING  {k}")
    for k in extra:
        print(f"EXTRA    {k}")
    for key, path, va, vb in config:
        print(f"CONFIG   {key}  {path}: baseline={va!r}  build={vb!r}")
    for key, path, va, vb in tags:
        print(f"TAG      {key}  {path}: baseline={va!r}  build={vb!r}")
    identical = not (missing or extra or config)
    print(f"\nSummary: missing={len(missing)} extra={len(extra)} config={len(config)} tags={len(tags)} "
          f"resources_with_config_diffs={len({c[0] for c in config})} identical={'yes' if identical else 'no'}")

    out = Path(__file__).resolve().parent / "comparisons.csv"
    new = not out.exists()
    with out.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["baseline", "build", "missing", "extra", "config_diffs", "tag_diffs",
                        "resources_with_config_diffs", "identical"])
        w.writerow([base["label"], build["label"], len(missing), len(extra), len(config), len(tags),
                    len({c[0] for c in config}), "yes" if identical else "no"])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
