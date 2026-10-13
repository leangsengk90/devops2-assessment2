# Rebuild timing summary (cycles 1–5, 13 Oct 2026, ap-southeast-2)

Each cycle: destroy deployments → infrastructures (ECR repos kept) → remote-state, then create remote-state → infrastructures → deployments and wait until all ECS services are healthy.
Cycle 6 was stopped partway by request and is excluded. Raw data: timings.csv, service-health.csv, logs/.

| Phase | C1 | C2 | C3 | C4 | C5 | Mean | Min | Max | SD |
|---|---|---|---|---|---|---|---|---|---|
| Destroy deployments (5 services) | 18m27s | 21m35s | 18m26s | 18m31s | 18m50s | 19m10s | 18m26s | 21m35s | 82s |
| Destroy infrastructures | 1m34s | 1m38s | 2m04s | 1m53s | 1m31s | 1m44s | 1m31s | 2m04s | 14s |
| Destroy remote-state | 19s | 19s | 19s | 22s | 18s | 19s | 18s | 22s | 2s |
| Create remote-state (plan+apply) | 1m14s | 1m14s | 1m15s | 1m15s | 1m15s | 1m15s | 1m14s | 1m15s | 1s |
| Create infrastructures (plan+apply) | 3m03s | 3m12s | 2m59s | 3m10s | 3m09s | 3m07s | 2m59s | 3m12s | 5s |
| Create deployments (5 services plan+apply) | 3m36s | 3m40s | 3m29s | 3m36s | 3m28s | 3m34s | 3m28s | 3m40s | 5s |
| Wait until all services healthy (after last apply) | 1m11s | 1m12s | 1m11s | 1m11s | 1m12s | 1m11s | 1m11s | 1m12s | 1s |
| Total cycle | 30m17s | 33m39s | 30m36s | 30m47s | 30m34s | 31m11s | 30m17s | 33m39s | 84s |

Full create from empty (remote-state → healthy services): mean ≈ 9m07s. Full destroy: mean ≈ 21m13s.

| Service | Time to healthy C1..C5 (s) | Mean | SD | HTTP |
|---|---|---|---|---|
| auth | 78, 81, 97, 96, 87 | 87.8 | 8.6 | 200 |
| messenger | 81, 82, 81, 79, 87 | 82.0 | 3.0 | 200 |
| profile | 74, 95, 111, 75, 93 | 89.6 | 15.5 | 200 |
| finance | 76, 110, 85, 76, 104 | 90.2 | 15.9 | 404 (app has no `/` handler) |
| share | 75, 79, 81, 74, 79 | 77.6 | 3.0 | 200 |

All services: n=25, mean 85.4s, SD 11.0s, min 74s, max 111s.
