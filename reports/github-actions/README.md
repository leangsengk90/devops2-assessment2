# Prod pipeline — GitHub Actions timeline

Pushing a change to `rebuild.sh` runs a full rebuild (destroy and recreate remote-state → infrastructures → deployments; ECR repositories and images are kept). Pushing a change to `redeploy.sh` only redeploys the microservices. Pushing a change to `destroy.sh` destroys everything, including the ECR repositories and images. This file is regenerated after every run; per-run details are in [`runs/`](runs/), raw data in `timings.csv` and `service-health.csv`.

## Rebuild runs

| Run | Date | Commit | Result | Destroy deploy | Destroy infra | Destroy state | Create state | Create infra | Create deploy | Healthy | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [#1](runs/run-0001.md) | 2026-10-14 01:13 | `95e368e` | success | 21m 35s | 1m 50s | 24s | 1m 22s | 3m 18s | 3m 03s | 1m 09s | 32m 41s |
| [#4](runs/run-0004.md) | 2026-10-14 08:48 | `dfbfafe` | success | 17m 49s | 1m 26s | 24s | 1m 09s | 2m 56s | 2m 43s | 1m 24s | 27m 52s |
| [#5](runs/run-0005.md) | 2026-10-14 11:01 | `1d07bb8` | success | 16m 59s | 1m 20s | 24s | 1m 09s | 2m 52s | 2m 32s | 1m 24s | 26m 40s |
| [#6](runs/run-0006.md) | 2026-10-14 13:56 | `e8a679b` | success | 18m 14s | 1m 21s | 22s | 1m 14s | 3m 04s | 2m 31s | 1m 55s | 28m 41s |
| [#7](runs/run-0007.md) | 2026-10-14 16:20 | `151efd3` | success | 17m 21s | 1m 32s | 19s | 1m 10s | 2m 57s | 2m 37s | 1m 08s | 27m 04s |
| [#8](runs/run-0008.md) | 2026-10-14 17:40 | `15ed68c` | success | 18m 45s | 1m 25s | 21s | 1m 09s | 3m 06s | 2m 45s | 53s | 28m 24s |

### Rebuild statistics over 6 successful run(s)

| Phase | Mean | Min | Max | SD |
|---|---|---|---|---|
| Destroy deployments | 18m 27s | 16m 59s | 21m 35s | 99s |
| Destroy infrastructures | 1m 29s | 1m 20s | 1m 50s | 11s |
| Destroy remote-state | 22s | 19s | 24s | 2s |
| Create remote-state | 1m 12s | 1m 09s | 1m 22s | 5s |
| Create infrastructures | 3m 02s | 2m 52s | 3m 18s | 9s |
| Create deployments | 2m 42s | 2m 31s | 3m 03s | 12s |
| Wait until healthy | 1m 19s | 53s | 1m 55s | 21s |
| Total | 28m 34s | 26m 40s | 32m 41s | 130s |

## Redeploy runs

| Run | Date | Commit | Result | Redeploy | Healthy | Total |
|---|---|---|---|---|---|---|
| [#2](runs/run-0002.md) | 2026-10-14 01:51 | `6a28fa3` | success | 2m 00s | 3m 00s | 5m 00s |

### Redeploy statistics over 1 successful run(s)

| Phase | Mean | Min | Max | SD |
|---|---|---|---|---|
| Redeploy deployments | 2m 00s | 2m 00s | 2m 00s | – |
| Wait until healthy | 3m 00s | 3m 00s | 3m 00s | – |
| Total | 5m 00s | 5m 00s | 5m 00s | – |
