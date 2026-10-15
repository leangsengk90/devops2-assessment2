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
| [#9](runs/run-0009.md) | 2026-10-14 19:30 | `4e5477f` | success | 17m 38s | 1m 32s | 21s | 1m 13s | 2m 55s | 2m 34s | 1m 24s | 27m 37s |
| [#10](runs/run-0010.md) | 2026-10-14 20:53 | `8368863` | success | 18m 13s | 1m 21s | 18s | 1m 09s | 3m 03s | 2m 32s | 1m 08s | 27m 44s |
| [#11](runs/run-0011.md) | 2026-10-14 22:12 | `fb6da05` | success | 18m 09s | 1m 35s | 24s | 1m 10s | 2m 57s | 2m 43s | 1m 24s | 28m 22s |
| [#12](runs/run-0012.md) | 2026-10-14 23:36 | `e48343f` | success | 18m 06s | 1m 22s | 22s | 1m 08s | 3m 04s | 2m 34s | 1m 23s | 27m 59s |
| [#13](runs/run-0013.md) | 2026-10-15 02:14 | `d659e9c` | success | 18m 38s | 1m 40s | 24s | 1m 12s | 3m 04s | 3m 01s | 1m 26s | 29m 25s |
| [#14](runs/run-0014.md) | 2026-10-15 02:51 | `cf5dd79` | success | 17m 20s | 1m 45s | 24s | 1m 09s | 2m 57s | 2m 40s | 1m 08s | 27m 23s |
| [#15](runs/run-0015.md) | 2026-10-15 03:36 | `d73ec12` | success | 17m 54s | 1m 31s | 23s | 1m 09s | 3m 02s | 2m 32s | 1m 08s | 27m 39s |
| [#16](runs/run-0016.md) | 2026-10-15 08:10 | `fc86389` | success | 19m 38s | 1m 35s | 24s | 1m 10s | 3m 06s | 2m 40s | 1m 08s | 29m 41s |
| [#17](runs/run-0017.md) | 2026-10-15 09:38 | `fa72284` | success | 19m 15s | 1m 25s | 19s | 1m 10s | 2m 56s | 2m 45s | 1m 39s | 29m 29s |
| [#18](runs/run-0018.md) | 2026-10-15 10:07 | `789c7b2` | success | 18m 52s | 1m 31s | 24s | 1m 12s | 3m 11s | 3m 03s | 1m 25s | 29m 38s |
| [#19](runs/run-0019.md) | 2026-10-15 10:38 | `fe10649` | success | 18m 32s | 1m 27s | 21s | 1m 22s | 3m 09s | 2m 52s | 1m 25s | 29m 08s |
| [#20](runs/run-0020.md) | 2026-10-15 11:07 | `16ef1f5` | success | 18m 51s | 1m 34s | 24s | 1m 15s | 3m 06s | 2m 41s | 1m 24s | 29m 15s |
| [#21](runs/run-0021.md) | 2026-10-15 11:37 | `8cc94e7` | success | 17m 31s | 1m 39s | 24s | 1m 11s | 3m 24s | 3m 01s | 1m 25s | 28m 35s |
| [#22](runs/run-0022.md) | 2026-10-15 12:06 | `7939475` | success | 17m 30s | 1m 34s | 24s | 1m 10s | 2m 58s | 2m 39s | 1m 09s | 27m 24s |
| [#23](runs/run-0023.md) | 2026-10-15 12:34 | `cbeb8b0` | success | 17m 20s | 1m 21s | 22s | 1m 08s | 3m 03s | 2m 31s | 1m 23s | 27m 08s |
| [#24](runs/run-0024.md) | 2026-10-15 13:01 | `bec2c30` | success | 18m 44s | 1m 18s | 24s | 1m 11s | 3m 12s | 2m 58s | 1m 25s | 29m 12s |
| [#25](runs/run-0025.md) | 2026-10-15 13:31 | `cad5f30` | success | 17m 08s | 1m 34s | 23s | 1m 10s | 3m 07s | 2m 41s | 1m 24s | 27m 27s |
| [#26](runs/run-0026.md) | 2026-10-15 13:59 | `451698e` | success | 17m 33s | 1m 35s | 21s | 1m 10s | 2m 59s | 2m 48s | 1m 40s | 28m 06s |
| [#27](runs/run-0027.md) | 2026-10-15 14:28 | `d2baed9` | success | 18m 08s | 1m 33s | 23s | 1m 16s | 3m 05s | 2m 44s | 1m 23s | 28m 32s |
| [#28](runs/run-0028.md) | 2026-10-15 14:57 | `ccec9a6` | success | 18m 25s | 1m 15s | 20s | 1m 15s | 2m 55s | 2m 41s | 1m 24s | 28m 15s |
| [#29](runs/run-0029.md) | 2026-10-15 15:25 | `976d908` | success | 17m 59s | 1m 39s | 25s | 1m 11s | 3m 03s | 3m 03s | 1m 10s | 28m 30s |

### Rebuild statistics over 27 successful run(s)

| Phase | Mean | Min | Max | SD |
|---|---|---|---|---|
| Destroy deployments | 18m 14s | 16m 59s | 21m 35s | 57s |
| Destroy infrastructures | 1m 30s | 1m 15s | 1m 50s | 8s |
| Destroy remote-state | 23s | 18s | 25s | 2s |
| Create remote-state | 1m 12s | 1m 08s | 1m 22s | 4s |
| Create infrastructures | 3m 03s | 2m 52s | 3m 24s | 7s |
| Create deployments | 2m 44s | 2m 31s | 3m 03s | 11s |
| Wait until healthy | 1m 21s | 53s | 1m 55s | 12s |
| Total | 28m 26s | 26m 40s | 32m 41s | 72s |

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
