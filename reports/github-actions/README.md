# Prod pipeline — GitHub Actions timeline

Pushing a change to `rebuild.sh` runs a full rebuild (destroy and recreate remote-state → infrastructures → deployments; ECR repositories and images are kept). Pushing a change to `redeploy.sh` only redeploys the microservices. This file is regenerated after every run; per-run details are in [`runs/`](runs/), raw data in `timings.csv` and `service-health.csv`.

## Rebuild runs

| Run | Date | Commit | Result | Destroy deploy | Destroy infra | Destroy state | Create state | Create infra | Create deploy | Healthy | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [#1](runs/run-0001.md) | 2026-10-14 01:13 | `95e368e` | success | 21m 35s | 1m 50s | 24s | 1m 22s | 3m 18s | 3m 03s | 1m 09s | 32m 41s |

### Rebuild statistics over 1 successful run(s)

| Phase | Mean | Min | Max | SD |
|---|---|---|---|---|
| Destroy deployments | 21m 35s | 21m 35s | 21m 35s | – |
| Destroy infrastructures | 1m 50s | 1m 50s | 1m 50s | – |
| Destroy remote-state | 24s | 24s | 24s | – |
| Create remote-state | 1m 22s | 1m 22s | 1m 22s | – |
| Create infrastructures | 3m 18s | 3m 18s | 3m 18s | – |
| Create deployments | 3m 03s | 3m 03s | 3m 03s | – |
| Wait until healthy | 1m 09s | 1m 09s | 1m 09s | – |
| Total | 32m 41s | 32m 41s | 32m 41s | – |

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
