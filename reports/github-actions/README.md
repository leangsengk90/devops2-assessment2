# Prod pipeline — GitHub Actions timeline

Pushing a change to `rebuild.sh` runs a full rebuild (destroy and recreate remote-state → infrastructures → deployments; ECR repositories and images are kept). Pushing a change to `redeploy.sh` only redeploys the microservices. Pushing a change to `destroy.sh` destroys everything, including the ECR repositories and images. This file is regenerated after every run; per-run details are in [`runs/`](runs/), raw data in `timings.csv` and `service-health.csv`.

## Rebuild runs

| Run | Date | Commit | Result | Destroy deploy | Destroy infra | Destroy state | Create state | Create infra | Create deploy | Healthy | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [#1](runs/run-0001.md) | 2026-10-14 01:13 | `95e368e` | success | 21m 35s | 1m 50s | 24s | 1m 22s | 3m 18s | 3m 03s | 1m 09s | 32m 41s |
| [#4](runs/run-0004.md) | 2026-10-14 08:48 | `dfbfafe` | success | 17m 49s | 1m 26s | 24s | 1m 09s | 2m 56s | 2m 43s | 1m 24s | 27m 52s |

### Rebuild statistics over 2 successful run(s)

| Phase | Mean | Min | Max | SD |
|---|---|---|---|---|
| Destroy deployments | 19m 42s | 17m 49s | 21m 35s | 160s |
| Destroy infrastructures | 1m 38s | 1m 26s | 1m 50s | 17s |
| Destroy remote-state | 24s | 24s | 24s | 0s |
| Create remote-state | 1m 16s | 1m 09s | 1m 22s | 9s |
| Create infrastructures | 3m 07s | 2m 56s | 3m 18s | 16s |
| Create deployments | 2m 53s | 2m 43s | 3m 03s | 14s |
| Wait until healthy | 1m 16s | 1m 09s | 1m 24s | 11s |
| Total | 30m 16s | 27m 52s | 32m 41s | 204s |

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
