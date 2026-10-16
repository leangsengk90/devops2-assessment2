# Manual provisioning test kit

This kit lets you time real manual console builds so they can replace the **simulated** manual data in the dissertation.

| File | What it's for |
|---|---|
| `STEP-BY-STEP.md` | **Start here:** click-by-click console instructions for the whole build, with troubleshooting |
| `CHECKLIST.md` | One-page tick list of the same build, to keep beside you while you work |
| `recording-sheet.csv` | Fill one row per run (opens in Excel) |
| `export.py` | Saves the configuration of whatever is currently built (read-only AWS calls) |
| `compare.py` | Compares a build with the Terraform baseline and counts differences (for H3) |
| `prepare.sh` | Empties the account before the first manual run (keeps ECR images) |
| `teardown-manual.sh` | Deletes a manual build between runs (dry run unless `CONFIRM=delete`) |

You need the AWS CLI logged in to the project account, Python 3, and Terraform for `prepare.sh`.

## Steps

**1. Export the Terraform baseline (once).**

Make sure no GitHub Actions run is in progress and all 5 services are healthy, then run:

```
python3 export.py terraform-baseline
```

The summary should say about 140 resources. The ECR repositories aren't exported because they aren't rebuilt.

**2. Empty the account (once).**

```
CONFIRM=destroy ./prepare.sh
```

**3. Do manual run N.**

Follow `STEP-BY-STEP.md` (with `CHECKLIST.md` to tick off) and a timer, and fill row N of `recording-sheet.csv`. Record:
- start and end time
- breaks
- mistakes you had to redo
- 5/5 services running
- 5/5 HTTP 200

**4. Export and compare before deleting anything.**

```
python3 export.py manual-run-N
python3 compare.py exports/terraform-baseline.json exports/manual-run-N.json
```

`identical=yes` means your build matches Terraform exactly. Each run adds a line to `comparisons.csv`.

**5. Delete the manual build.**

First check what will be deleted, then delete:

```
./teardown-manual.sh
CONFIRM=delete ./teardown-manual.sh
```

If something fails because it's still in use, wait a minute and run it again. Then repeat from step 3 for the next run.

**6. After the last run, restore Terraform prod.**

Run teardown one last time, then from the repository root run `./rebuild.sh`. That recreates everything with Terraform and re-attaches the ECR repositories.

## How many runs

- **3:** the minimum for a statistical test.
- **10:** ideal; matches the proposal and the 10 pipeline runs.

Each run takes about 1.5–2 hours, plus about 15 minutes for teardown.

## What to send back

- `recording-sheet.csv`
- the `exports/` folder
- `comparisons.csv`

I'll replace the simulated manual data with your real data and update Chapters 3–6, the abstract and the slides.

## Tips

- **Same order every run.** Don't improvise; the comparison measures your consistency.
- **What counts as a mistake:** any resource you had to fix after creating it. Write a few words in `what_went_wrong`. These notes become qualitative evidence.
- **Expect some console differences.** Console defaults sometimes differ from Terraform's (for example, ECS deployment circuit breaker settings). `compare.py` lists every difference by name. Send the output and we'll decide together which are your mistakes and which are console defaults; the dissertation will report both.
- **NAT gateways cost money per hour.** Don't leave a manual build running overnight.
