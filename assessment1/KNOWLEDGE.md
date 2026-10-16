# Assessment 1 digest — `KAO_Leangseng_ITRM_Assessment1_v2.docx`

Research proposal (Chapters 1–3 plus references and appendices) for the IT Research Methodology course, written on the UP dissertation template (see `resources/KNOWLEDGE.md`). Assessment 2 presumably delivers Chapters 4–5 (results, then discussion and conclusions) using the data this repo produces. Chapter 1.10 says the dissertation has **five** chapters, not the template's six: Chapter 5 combines discussion, conclusions, contributions, limitations and recommendations.

## Identity

- **Student:** KAO LEANGSENG, ID UPS240590. **Supervisor:** Dr. CHEN SOVANN. **Degree:** MSc in Information Technology. **Faculty:** Science and Technology, University of Puthisastra. Dated 22 August 2026.
- **Title on the cover:** *Evaluating the Effectiveness of Terraform and GitHub Actions for AWS Infrastructure Automation*.
- **Title in the declaration and approval pages:** *Infrastructure as Code for a Containerised AWS Architecture: Implementing and Evaluating Terraform within a GitHub Actions CI/CD Pipeline*. The two titles don't match.
- **Case:** an unnamed Cambodian financial institution supervised by the National Bank of Cambodia (NBC). Work runs in an isolated sandbox AWS account. The organisation must not be named, and no account IDs, resource names, IP ranges or IAM policies may be published.

## Problem, gap and aim

- **Problem:** the app CI/CD (build → test → static scan → ECR push and scan) is automated, but the AWS infrastructure is built by hand in the console. As a result there is no audit trail, the dev, staging and prod environments drift apart, and rebuilding depends on what engineers remember.
- **Three gaps:**
  - **Empirical:** existing studies compare IaC tool against IaC tool (Regvart 2026), never IaC against manual provisioning.
  - **Theoretical:** IaC and CI/CD are studied separately. The proposal argues the governance benefit comes from the review gate, not the file format, so it adds **pipeline integration depth** as a moderator.
  - **Contextual:** there is no IaC evidence from Cambodia or Southeast Asia.
- **Aim:** build modular Terraform for a containerised AWS architecture, integrate it into GitHub Actions, and measure provisioning duration, drift, reproducibility and version-control coverage against manual provisioning. Then explain the barriers encountered.

## Objectives, research questions and hypotheses

**Objectives**
- O1: inventory the current architecture.
- O2: build Terraform modules with an S3 backend and DynamoDB locking, parameterised so one codebase serves 3 environments.
- O3: pipeline integration with validate, plan on every PR, and a gated apply on merge.
- O4: measure the outcomes and test significance.
- O5: identify barriers and enablers, and make recommendations.

**Research questions**
- RQ1: current provisioning and version-control coverage (descriptive).
- RQ2: Terraform vs manual on the 4 outcomes.
- RQ3: does integration depth moderate the method → drift relationship?
- RQ4: barriers and enablers (qualitative).

**Hypotheses**, all tested at p < .05 with effect sizes:

| H | Claim | Planned test |
|---|---|---|
| H1 | Terraform provisioning duration < manual | Welch t **and** Mann–Whitney U, Cohen's d with CI |
| H2 | Terraform drift < manual | Fisher's exact |
| H3 | Terraform destroy-and-rebuild success rate > manual | Fisher's exact; proportions with CIs |
| H4 | Pipeline integration raises version-control/peer-review coverage | descriptive census (no inferential test); list partial definitions separately |
| H5 | Integration depth moderates method → drift | Kruskal–Wallis across 3 depth levels; low power acknowledged in advance |

**Conceptual framework (Fig 2.1):** independent variable = provisioning method (Terraform vs manual console). Dependent variables: DV1 duration, DV2 drift, DV3 reproducibility, DV4 version-control coverage. Moderator = pipeline integration depth. Controls = region, time of day, run order.

**Integration depth levels:** (1) local run with no review, (2) validate and plan on PR, (3) validate, plan and gated apply on merge.

## Theory and literature

- **Framework:** IaC principles (declarative specification, idempotence, version control; Kumara 2021, Guerriero 2019), plus the deployment-pipeline concept (Hilton 2016), plus DevOps capability measurement logic (borrows the DORA idea, not its metrics).
- **TAM, UTAUT, DOI and TPB were deliberately rejected**, because their unit of analysis is a person's perception and this study's dependent variables are system properties. Their "facilitating conditions" idea is used only to frame RQ4.

**The 5 core studies**
- **Regvart, Vlahović & Balković (2026):** Terraform vs Pulumi vs CloudFormation, 30 runs each.
  - Provisioning: Terraform 253.33 s (SD 8.42), Pulumi 279.37 (SD 9.89), CloudFormation 622.97 (SD 29.92).
  - Destroy: 466.23 / 513.73 / 578.40 s.
  - No failures. This is the procedural template this study copies.
- **Verdet et al. (2025):** 812 Terraform projects scanned with Checkov and tfsec. Access policy is the most applied; encryption at rest the most neglected.
- **Begoug, Ouni & Chouchen (2025):** Terraform module updates are postponed and technical lag lasts months. This is the justification for pinning versions.
- **Rostami Mazrae et al. (2023):** 22 interviews. 18 of the 22 use GitHub Actions; 17 of 32 tool migrations went towards it. The main barrier is the YAML learning curve plus the commit-push-wait loop, because workflows can't be tested locally.
- **Villamizar et al. (2017):** monolith vs microservices vs Lambda on AWS. Cost falls about 9.5–13.8% for customer-operated microservices and 70% or more for Lambda in the best case.

**Supporting studies:** Hilton 2016 (CI projects release 0.54 vs 0.24 times per month), Guerriero 2019 (44 companies; hardcoded credentials named the worst practice), Kumara 2021 (taxonomy of 10 good-practice and 4 bad-practice categories).

**Excluded:** the "50% deployment-time reduction" claim, because it can't be verified.

## Methodology commitments

- **Approach:** pragmatism; abductive reasoning; explanatory sequential mixed methods.
  - Phase 1: controlled repeated-deployment experiment.
  - Phase 2: reflexive thematic analysis (Braun & Clarke) of a **structured implementation log** plus PR review comments.
  - Phase 3: joint display (Fetters 2013), in which divergence is reported, not reconciled.
- **No human participants**, so there is no survey; Cronbach's α and CR don't apply.
- **Runs:**
  - 30 Terraform, 10 manual (about 45 min each, done **before** module development to avoid a learning effect, following a written console procedure).
  - 10 destroy-and-rebuild cycles per method.
  - 3 environments, giving 3 pairwise drift comparisons per method and per depth level.
  - 5 pilot runs on the VPC module only. The pilot includes a **deliberate-difference sensitivity test**, confirming the drift tool catches a planted difference.
  - Run order randomised with a recorded seed and interleaved.
  - Power analysis: d = 0.8 needs about 26 per group; the expected effect is d > 1.5.
- **Instruments:**
  - Duration: a shell script writing Unix timestamps per stage to CSV (`run, condition, stage, start, end, seconds`). Terraform stages are init, plan, apply and destroy.
  - Drift: `terraform plan` output plus an AWS CLI attribute inventory, judged against an intentional-difference list written in advance.
  - Reproducibility: inventory before vs after a rebuild; success means zero unintended differences.
  - Coverage: components classed as fully, partially or not defined, divided by the inventory count.
  - Secondary measure: Checkov/tfsec failed checks.
- **Controls:** same account, region, credentials, machine and wired network; verified empty start state; tool versions recorded every run (Terraform, provider, runner image); timing script calibrated to within 1 s.
- **Analysis:** Python (pandas, SciPy, statsmodels); Shapiro–Wilk, skewness and kurtosis. Outliers are inspected, not auto-removed. Excluded runs are reported with their reasons.
- **Ethics:** organisational consent; UP committee confirmation that no approval is needed (Appendix D); no production or customer data; **GitHub OIDC short-lived credentials, no long-lived keys**; secrets injected at runtime; budget alarm; destroy after each cycle; total spend reported.
- **Limitations:** single case; 10 vs 30 runs with a learning effect; researcher not independent and expecting Terraform to win; only a 12-week window (can't observe module maintenance cost); tool versions keep changing.
- **Timeline (Table 3.5), 12 weeks July–September 2026:**
  - Wk 1–3: prep. Wk 3: manual baseline. Wk 4: pilot.
  - Wk 4–7: modules. Wk 7–8: CI integration.
  - Wk 9–10: measurement campaign. Wk 10: analysis.
  - Wk 11: thematic analysis. Wk 12: integration and write-up.
- **Appendices:** A component inventory template; B implementation log template; C measurement scripts; D institutional approval; E timeline; F leftover template notes.

## Proposal vs what this repo actually implements (check before writing Assessment 2)

| Proposal said | Repo reality |
|---|---|
| 3 environments (dev/staging/prod) from one parameterised codebase | Only the `prod` workspace is used (`remote-state` also has `preprod` state). Workspaces + `terraform.workspace` naming would support more |
| Validate + plan on every PR + gated apply on merge (depth level 3); branch protection | `rebuild-prod.yml` runs on **push to main** with `-auto-approve`; no PR plan job, no `terraform validate`/`fmt` step, no manual approval gate |
| OIDC short-lived credentials | Workflow uses `secrets.AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` (long-lived keys) |
| Checkov/tfsec security scans | Not present; only ECR image scanning via Inspector |
| Architecture incl. WAF, Route 53, TLS certificates, NAT/IGW, API GW + VPC Link, ECS Fargate, ALB, IAM, alarms, scaling | VPC/NAT/IGW, ALB, API Gateway HTTP + VPC Link, ECS Fargate ×5 services with autoscaling and alarms, ECR ×6, IAM, CloudWatch, Inspector, S3+DynamoDB state. **No WAF, Route 53 or TLS** (ALB listener is HTTP) |
| 30 Terraform runs with per-stage init/plan/apply/destroy timings | `reports/github-actions/timings.csv`: **30 successful full rebuilds** (runs #1, #4–#16 push-triggered on 2026-10-14/15; #17–#32 chained `workflow_dispatch` on 2026-10-15) + 1 redeploy, timed per *phase* (destroy deployments/infra/state, create state/infra/deployments, wait healthy). Full create mean 499.8 s (SD 21.0, CV 4.2%); full destroy 1207 s; cycle ≈ 28m27s. Dispatched runs built ~18 s slower (p = .019); no trend by run order, day or hour. Analysis in `assessment2/analysis/results.json`. `service-health.csv` has seconds-to-healthy and HTTP code per service |
| Fixed versions recorded | Terraform 1.13.3 pinned in CI; AWS provider `~> 5.0` (not exact) in infra/deployments, `6.20.0` in remote-state; `.terraform.lock.hcl` is gitignored; container image tag hard-coded `:15` |
| Region | `ap-southeast-2` (Sydney), account 029637202701. Do not publish these in the dissertation |
| Manual baseline, drift, reproducibility and coverage measurements | Not in the repo; there's no data for them yet |

## Writing issues spotted in v2 (fix before or alongside Assessment 2)

- Cover title ≠ declaration/approval title.
- §3.12 calls it a "bachelor's dissertation"; the degree is a Master's.
- The acknowledgements say "Faculty of Information Technology"; the cover says Science and Technology.
- §1.8 says "Temporarily"; it should be "Temporally".
- Table 3.2 is still titled "Questionnaire Constructs, Items and Sources", though it lists instruments.
- The references preamble still contains the template's placeholder sentence.
- Appendix F "Notes on Using This Template" is still included.
- Table of contents is empty (fields not updated).
- Figure 2.1 places the H5 dashed arrow near the H1 path, but H5 moderates the **drift (H2)** path.
- H2 uses Fisher's exact test on attribute *counts*. Fisher's exact suits categorical counts (e.g. drifted vs not), so either dichotomise per attribute or use a count test (e.g. Mann–Whitney or Poisson).
- Abstract and design say "will"; Assessment 2 must switch to past tense for what was done.
