import json
from pathlib import Path
from docxlib import h1, h2, h3, p, li, caption, table, note, figcap

R = json.loads((Path(__file__).resolve().parent.parent / "analysis" / "results.json").read_text())
G = R["gh_phases"]
S = R["sim_manual"]
H1 = R["h1"]
TF = G["Full create"]
mn = lambda s: f"{s / 60:.1f}"
f1 = lambda x: f"{x:.1f}"
pv = lambda x: "< .001" if x < .001 else f"{x:.3f}".lstrip("0")
TFmin = TF["mean"] / 60

phase_rows = []
for ph in ["Destroy deployments", "Destroy infrastructures", "Destroy remote-state", "Create remote-state",
           "Create infrastructures", "Create deployments", "Wait until healthy", "Full create", "Full destroy", "Total cycle"]:
    d = G[ph]
    phase_rows.append([ph, f"{d['mean']:.1f} ({d['sd']:.1f})", mn(d["mean"]), f"{d['median']:.0f}", f"{d['min']:.0f}–{d['max']:.0f}", f"{d['cv_pct']:.1f}"])

sim_rows = [[str(r["run"]), mn(r["hands_on_s"]), mn(r["wait_s"]), mn(r["full_create_s"]), str(r["reworked_resources"]),
             "Yes" if r["rebuild_success"] else f"No ({r['rebuild_attr_errors']} differing)"] for r in R["sim_manual_runs"]]

sens_rows = [[f"{k} s", f"{v:.1f}", f"{v / TFmin:.1f}"] for k, v in R["h1_sensitivity"].items()]
hb = R["health_by_service"]
names = {"auth": "Authentication", "messenger": "Messenger", "profile": "Profile", "finance": "Finance", "share": "Share"}
man = R["man_rebuild_success"]
N = R["n_tf"]
NW = {30: "thirty", 10: "ten"}.get(N, str(N))
REC = R["record"]
C = R["campaign"]
TRG = R["trigger"]
DAY = R["by_day"]
TR = R["trend"]
HR = R["hour"]
OUT = R["outliers"]
F10 = R["first10"]["Full create"]
miss = R["health_missing"][0]
hm = R["health_max_at"]
svc_name = {"auth": "authentication", "messenger": "messenger", "profile": "profile", "finance": "finance", "share": "share"}
nonnormal = [ph for ph in ["Destroy deployments", "Destroy infrastructures", "Destroy remote-state", "Create remote-state",
                           "Create infrastructures", "Create deployments", "Wait until healthy"] if G[ph]["shapiro_p"] < .05]
sw = lambda d: f"_W_ = {d['shapiro_W']:.2f}, _p_ {'< .001' if d['shapiro_p'] < .001 else '= ' + pv(d['shapiro_p'])}"
def pp(x):
    return f"_p_ {pv(x)}" if x < .001 else f"_p_ = {pv(x)}"
def welch(t):
    return f"_t_({t['welch_df']:.1f}) = {t['welch_t']:.2f}, {pp(t['welch_p'])}"
plain = lambda s: s.replace("_", "")
stab_rows = []
for lab, d in [("Full build", "Full create"), ("Full destroy", "Full destroy"), ("Total cycle", "Total cycle")]:
    t = TRG[d]
    stab_rows.append([f"{lab}: push vs. dispatch", f"{t['push']['mean']:.1f} vs. {t['dispatch']['mean']:.1f}",
                      plain(f"t({t['test']['welch_df']:.1f}) = {t['test']['welch_t']:.2f}; U = {t['test']['mw_U']:.0f}"),
                      plain(f"{pv(t['test']['welch_p'])}; {pv(t['test']['mw_p'])}"), f"{t['test']['hedges_g']:.2f}"])
for lab, d in [("Full build", "Full create"), ("Total cycle", "Total cycle")]:
    t = DAY[d]
    stab_rows.append([f"{lab}: 14 Oct vs. 15 Oct", f"{t['day1']['mean']:.1f} vs. {t['day2']['mean']:.1f}",
                      plain(f"t({t['test']['welch_df']:.1f}) = {t['test']['welch_t']:.2f}; U = {t['test']['mw_U']:.0f}"),
                      plain(f"{pv(t['test']['welch_p'])}; {pv(t['test']['mw_p'])}"), f"{t['test']['hedges_g']:.2f}"])
for lab, d in [("Full build", "Full create"), ("Full destroy", "Full destroy"), ("Total cycle", "Total cycle")]:
    stab_rows.append([f"{lab}: run order", "—", f"ρ = {TR[d]['rho']:.2f}", pv(TR[d]['p']), "—"])
for lab, d in [("Full build", "Full create"), ("Total cycle", "Total cycle")]:
    stab_rows.append([f"{lab}: hour of day", "—", f"ρ = {HR[d]['rho']:.2f}", pv(HR[d]['p']), "—"])
out_txt = "; ".join(f"{ph.lower()} (run{'s' if len(v) > 1 else ''} {', '.join(map(str, v))})" for ph, v in OUT.items() if v and ph not in ("Full destroy", "Total cycle"))

BLOCKS = [
h1("CHAPTER 4: RESULTS AND FINDINGS"),
h2("4.1 Introduction"),
p("This chapter presents the results of the study. It reports the completeness of the data, describes the architecture and the measurement runs, and answers RQ1 through the component inventory. It then reports the measured durations and service recovery of the Terraform pipeline, the simulated manual condition, the tests applied to each hypothesis (RQ2) and the integration level achieved (RQ3). The qualitative findings follow (RQ4), and the chapter closes by integrating the two strands. Results are reported without interpretation; their meaning is discussed in Chapter 5."),
p("Statistics are reported in accordance with the seventh edition of the APA Publication Manual (American Psychological Association, 2020). **All values for the manual condition are simulated** from the model described in Section 3.7.1 and are labelled as such in every table and figure. All values for the Terraform condition are measured. Every figure can be regenerated from the raw files and the seeded simulation by the analysis script listed in Appendix C."),
h2("4.2 Data Completeness and Screening"),
h3("4.2.1 Completeness of Measurement Runs"),
p(f"Thirty-one rebuild runs were triggered in GitHub Actions between {C['first']} and {C['last_start']} (local time). Thirty completed and wrote a run report. The remaining run (run 3) produced no report because the step that commits the report back to the repository failed; the fault was corrected in the next commit, but the provisioning outcome of that run was not recorded, so it was excluded. One further run (run 2) was a redeploy rather than a rebuild and is reported separately in Section 4.7. Of the {N} analysed cycles, {C['push']} (runs 1 and 4–16) were triggered by a commit to the rebuild script and {C['dispatch']} (runs {C['dispatch_runs']}) by the chained manual-dispatch event; {C['per_day']['14 Oct']} ran on 14 October and {C['per_day']['15 Oct']} on 15 October. The analysed Terraform sample is therefore {N} complete rebuild cycles and {R['n_starts']} service start-ups. The simulated manual condition comprises 10 builds and 10 rebuilds generated with seed 20261015."),
caption("Table 4.1", "Measurement Runs Collected, Excluded and Analysed"),
table(["Condition", "Date", "Runs", "Excluded (reason)", "Analysed"], [
    ["Terraform via GitHub Actions: rebuild, push-triggered", "14–15 Oct 2026", "15", "Run 3 (report commit failed; outcome unrecorded)", f"{C['push']} cycles; {5 * C['push']} service start-ups"],
    ["Terraform via GitHub Actions: rebuild, chained dispatch", "15 Oct 2026", str(C['dispatch']), "None", f"{C['dispatch']} cycles; {5 * C['dispatch']} service start-ups"],
    ["Terraform via GitHub Actions: redeploy", "14 Oct 2026", "1", "None", "Reported separately (Section 4.7)"],
    ["Manual console (SIMULATED)", "Oct 2026", "10 builds; 10 rebuilds", "None", "10 simulated builds; 10 simulated rebuilds"],
], [2500, 1200, 1300, 2240, 1400]),
h3("4.2.2 Data Screening"),
p(f"The timing files contained no missing or malformed rows, and every phase of every analysed cycle completed with status \"ok\". The service-health file had one missing value: in run {miss['run']} the {miss['service']} service answered HTTP {miss['http_code']} through the API Gateway, but ECS had not yet logged a steady-state event when the pipeline collected the record, so its start-up time is missing. It was treated as missing, not as a failure, leaving {R['health']['n']} timed start-ups. Tukey's fences flagged a small number of phase outliers: {out_txt}. All of them completed with status \"ok\", each was within 40% of its phase median (the largest relative excess being run 6’s wait for healthy services, 115 s against 84 s), and none indicated a measurement fault, so all were retained. The longest deployment-destroy phase ({G['Destroy deployments']['max']:.0f} s) occurred in run {R['destroy_deploy_max_run']}, the first run of the new workflow, which also produced the longest full cycle. The longest service start-up ({R['health']['max']:.0f} s, the {svc_name[hm['service']]} service in run {hm['run']}) was a single observation; the next longest was {R['health_second_max']:.0f} s."),
h2("4.3 Profile of the Architecture and Measurement Runs"),
p("Table 4.2 profiles the architecture as Terraform manages it, counted from the configuration. A full rebuild destroyed and recreated 140 resources; the 12 ECR resources (six repositories and their lifecycle policies) were deliberately retained so that container images survived each rebuild. The simulated manual builds create the same 140 resources."),
caption("Table 4.2", "Terraform Stacks and Managed Resources"),
table(["Stack", "Main contents", "Resources", "Recreated each cycle"], [
    ["Remote state", "S3 bucket (versioning, encryption, public-access block, lifecycle, CORS); DynamoDB lock table", "7", "Yes"],
    ["Shared infrastructure", "VPC, 4 subnets, Internet Gateway, 2 NAT gateways and Elastic IPs, route tables, 3 security groups and 7 rules, ALB and listener, API Gateway, stage and VPC Link, 2 IAM roles and policies, 2 log groups, alert topic and event rule", "43", "Yes"],
    ["Shared infrastructure (ECR)", "6 container repositories and lifecycle policies", "12", "No (retained)"],
    ["Each of 5 services", "Target group, listener rule, ECS cluster, task definition, Fargate service, scaling target, 4 scaling policies, 4 alarms, 2 API integrations and 2 routes", "18 (90 in total)", "Yes"],
    ["Total", "", "152", "140"],
], [2000, 4240, 1100, 1300]),
h2("4.4 Version-Control Coverage and Current Provisioning (RQ1)"),
p("RQ1 asked how the target architecture is provisioned and what proportion of its components are under version control. Before the study every component was created by hand in the AWS console and none was defined in the repository, so coverage was 0%. After implementation, 19 of the 24 inventory components (79.2%) were fully defined in Terraform or in the workflow file, 2 (8.3%) were partially defined, and 3 (12.5%) were not defined (Table 4.3). Including partial definitions, coverage was 87.5%."),
p("The two partially defined components are switched off in code rather than missing: the Inspector module creates the alert topic and event rule but its scanning enabler is disabled with the comment that Inspector \"is blocked by an SCP on the AWS Free plan account\", and the ALB and API Gateway modules support a TLS certificate and custom domain through optional variables that are not set, so the load balancer listener serves plain HTTP. The three undefined components are the Web Application Firewall, the Route 53 DNS records and the repository's branch-protection and review rules."),
p(f"On the peer-review half of RQ1, none of the {R['record']['human']} human-authored commits in the repository history passed through a pull request: the history contains no merge commits, and every change was pushed directly to the main branch. Infrastructure changes were therefore version-controlled but not peer-reviewed."),
caption("Table 4.3", "Component Inventory and Codification Status"),
table(["Component", "Status", "Component", "Status"], [
    ["VPC", "Full", "Auto scaling targets and policies", "Full"],
    ["Public and private subnets (2 AZs)", "Full", "CloudWatch alarms", "Full"],
    ["Internet Gateway", "Full", "CloudWatch log groups", "Full"],
    ["NAT gateways and Elastic IPs", "Full", "ECR repositories and lifecycle policies", "Full"],
    ["Route tables and associations", "Full", "API Gateway, stage and VPC Link", "Full"],
    ["Security groups and rules", "Full", "API Gateway routes and integrations", "Full"],
    ["ALB and listener", "Full", "IAM roles and policies", "Full"],
    ["Target groups and listener rules", "Full", "Terraform remote state (S3, DynamoDB)", "Full"],
    ["ECS clusters", "Full", "CI/CD pipeline definition", "Full"],
    ["ECS task definitions and Fargate services", "Full", "Inspector scanning and alert topic", "Partial"],
    ["Web Application Firewall", "None", "TLS certificate binding and custom domain", "Partial"],
    ["Route 53 DNS records", "None", "Branch protection and review rules", "None"],
], [2800, 1000, 3840, 1000]),
note("Full = 19 (79.2%); Partial = 2 (8.3%); None = 3 (12.5%); N = 24. Before the study all 24 were created manually (0% coverage)."),
h2("4.5 Terraform Pipeline Durations"),
p(f"Table 4.4 reports descriptive statistics for every phase of the {NW} measured pipeline rebuilds. Building the full environment from empty (remote state, shared infrastructure, five services and waiting until all services were stable) took a mean of {TF['mean']:.1f} s ({mn(TF['mean'])} min; _SD_ = {TF['sd']:.1f}; 95% CI [{TF['ci_low']:.1f}, {TF['ci_high']:.1f}]). Destroying the environment took {G['Full destroy']['mean']:.1f} s ({mn(G['Full destroy']['mean'])} min), and a complete destroy-and-rebuild cycle took {mn(G['Total cycle']['mean'])} minutes. The build was consistent: its coefficient of variation was {TF['cv_pct']:.1f}%. Destroying the five service stacks accounted for {R['destroy_deploy_share_pct']:.1f}% of the cycle, about {R['destroy_deploy_per_service_s'] / 60:.1f} minutes per service stack."),
caption("Table 4.4", f"Descriptive Statistics of Pipeline Rebuild Phases (Seconds, n = {N}, Measured)"),
table(["Phase", "M (SD)", "Minutes", "Mdn", "Range", "CV %"], phase_rows, [2840, 1500, 1000, 900, 1400, 1000]),
note("CV = coefficient of variation. The total cycle is the workflow's own elapsed time and includes initialisation between phases."),
("fig", "fig4_1_phase_durations.png", 6.0),
figcap(f"Figure 4.1. Mean duration of each phase of the {NW} measured GitHub Actions rebuilds; whiskers show one standard deviation."),
p(f"Figure 4.2 plots the full-build and full-cycle durations against run order, with each run coloured by its trigger and a band of two standard deviations around each mean. Neither series shows a trend over the {N} runs (full build ρ = {TR['Full create']['rho']:.2f}, {pp(TR['Full create']['p'])}; full cycle ρ = {TR['Total cycle']['rho']:.2f}, {pp(TR['Total cycle']['p'])}). Run 1 is the only cycle outside the band, after which durations settled. Adding twenty cycles to the first ten changed the mean full build by {abs(TF['mean'] - F10['mean']):.1f} s (from {F10['mean']:.1f} s to {TF['mean']:.1f} s) and narrowed its 95% confidence interval from ±{(F10['ci_high'] - F10['ci_low']) / 2:.1f} s to ±{(TF['ci_high'] - TF['ci_low']) / 2:.1f} s."),
("fig", "fig4_2_run_order.png", 6.0),
figcap(f"Figure 4.2. Full-build and full destroy-and-rebuild durations of the {NW} measured rebuilds in run order. Blue: triggered by a push; orange: chained manual dispatch. Shaded bands show the mean ± 2 SD; the dashed line separates the two days."),
h2("4.6 Stability Checks and Assumption Testing"),
h3("4.6.1 Stability of the Measured Sample"),
p(f"Before the cycles were pooled, four checks examined whether the conditions under which they ran affected the timings (Table 4.5). No difference between the triggers was detected in the full destroy or the total cycle (total cycle {TRG['Total cycle']['push']['mean']:.1f} s for push-triggered runs against {TRG['Total cycle']['dispatch']['mean']:.1f} s for dispatched runs, Welch's {welch(TRG['Total cycle']['test'])}). The full build, however, was {TRG['Full create']['dispatch']['mean'] - TRG['Full create']['push']['mean']:.1f} s ({(TRG['Full create']['test']['ratio'] - 1) * 100:.1f}%) longer in the dispatched runs ({TRG['Full create']['push']['mean']:.1f} s against {TRG['Full create']['dispatch']['mean']:.1f} s; Welch's {welch(TRG['Full create']['test'])}; Mann–Whitney _U_ = {TRG['Full create']['test']['mw_U']:.0f}, {pp(TRG['Full create']['test']['mw_p'])}; Hedges' _g_ = {abs(TRG['Full create']['test']['hedges_g']):.2f})."),
p(f"Trigger is confounded with time: every dispatched run took place on the second day, back to back, while the push-triggered runs were spread across both days with gaps between them. Comparing the days directly gave a difference in the same direction that was not significant (full build {DAY['Full create']['day1']['mean']:.1f} s against {DAY['Full create']['day2']['mean']:.1f} s; Welch's {welch(DAY['Full create']['test'])}), and neither run order nor hour of day was correlated with any duration. The difference most plausibly reflects AWS and runner conditions during the back-to-back runs rather than the trigger itself, which does not change the steps executed, although the design cannot separate the two. It is small in practical terms, about a third of a minute against a build of {TFmin:.1f} minutes, and two orders of magnitude smaller than the difference tested under H1, so the {N} cycles were pooled."),
caption("Table 4.5", "Stability Checks on the Measured Terraform Cycles"),
table(["Comparison", "Means (s)", "Statistic", "p (Welch; M–W)", "Hedges' g"], stab_rows, [2700, 1700, 2100, 1300, 840], sz=18),
note(f"Push-triggered n = {C['push']}; dispatch-triggered n = {C['dispatch']}; 14 Oct n = {C['per_day']['14 Oct']}; 15 Oct n = {C['per_day']['15 Oct']}. Group comparisons report Welch's t and the Mann–Whitney U, with their p values in that order. Run-order and hour-of-day rows report Spearman's ρ."),
h3("4.6.2 Distributional Assumptions"),
p(f"With thirty cycles the full build no longer departed from normality ({sw(TF)}), but Shapiro–Wilk tests indicated departures in {['no', 'one', 'two', 'three', 'four', 'five', 'six', 'all'][len(nonnormal)]} of the seven phases: " + ", ".join(f"{ph.lower()} ({sw(G[ph])})" for ph in nonnormal) + f". The full destroy ({sw(G['Full destroy'])}) and total cycle ({sw(G['Total cycle'])}) were positively skewed by run 1. The simulated manual build times did not depart from normality ({sw(S)}). Because some measured distributions are non-normal and the simulated group is small, H1 is reported with both Welch's _t_-test and the Mann–Whitney _U_ test. Common method bias is not applicable because no variable was self-reported."),
h2("4.7 Service Recovery Analysis"),
p(f"All {R['n_starts']} service start-ups in the {NW} rebuilds came back into service: {R['health']['n']} reached a recorded ECS steady state, and the remaining one (run {miss['run']}, {miss['service']}) answered HTTP 200 before its steady-state event was logged. The time from service creation to steady state averaged {R['health']['mean']:.1f} s (_SD_ = {R['health']['sd']:.1f}; 95% CI [{R['health']['ci_low']:.1f}, {R['health']['ci_high']:.1f}]; range {R['health']['min']:.0f}–{R['health']['max']:.0f} s). The authentication and finance services were the slowest and most variable; the share service was the fastest. All {R['n_http']} HTTP requests made through the API Gateway ({R['n_starts']} in rebuilds, 5 in the redeploy run) returned status 200. The redeploy run replaced all five services without rebuilding infrastructure in 300 s (120 s to redeploy and 180 s to become healthy)."),
caption("Table 4.6", "Time from Service Creation to Steady State by Service (Seconds, Measured)"),
table(["Service", "n", "M (SD)", "Range", "HTTP 200"],
      [[names[s], str(hb[s]['n']), f"{hb[s]['mean']:.1f} ({hb[s]['sd']:.1f})", f"{hb[s]['min']:.0f}–{hb[s]['max']:.0f}", f"{N} / {N}"] for s in names] +
      [["All services", str(R['health']['n']), f"{R['health']['mean']:.1f} ({R['health']['sd']:.1f})", f"{R['health']['min']:.0f}–{R['health']['max']:.0f}", f"{R['n_starts']} / {R['n_starts']}"]],
      [2200, 1000, 2000, 1640, 1800]),
note(f"n = timed start-ups. One finance start-up (run {miss['run']}) has no recorded steady-state event and is excluded from the timings but counted in the HTTP column."),
("fig", "fig4_3_time_to_healthy.png", 6.0),
figcap(f"Figure 4.3. Time from service creation to ECS steady state for each start-up in the {NW} measured rebuilds; horizontal bars mark the mean."),
h2("4.8 Hypothesis Testing (RQ2)"),
p("RQ2 asked how Terraform-based provisioning differs from manual provisioning. Table 4.7 lists the ten simulated manual runs; Table 4.9 summarises the decision for each hypothesis."),
caption("Table 4.7", "Simulated Manual Console Runs (SIMULATED, Seed 20261015)"),
table(["Run", "Hands-on (min)", "Waiting (min)", "Full build (min)", "Resources redone", "Rebuild identical?"], sim_rows, [700, 1500, 1400, 1500, 1500, 2040]),
note("Simulated values generated by the model in Section 3.7.1. They are not observations."),
h3("4.8.1 Provisioning Duration (H1)"),
p(f"The measured Terraform build averaged {TFmin:.1f} minutes over {N} cycles. The simulated manual build averaged {mn(S['mean'])} minutes (_SD_ = {S['sd'] / 60:.1f}; range {mn(S['min'])}–{mn(S['max'])}), {H1['ratio']:.1f} times longer. On the simulated data the difference was significant, Welch's _t_({H1['welch_df']:.1f}) = {H1['welch_t']:.2f}, _p_ {pv(H1['welch_p']) if H1['welch_p'] < .001 else '= ' + pv(H1['welch_p'])}; Mann–Whitney _U_ = {H1['mw_U']:.0f}, _p_ {pv(H1['mw_p'])}; Hedges' _g_ = {H1['hedges_g']:.2f}, 95% CI [{H1['g_ci_low']:.2f}, {H1['g_ci_high']:.2f}]. Because the spread of the simulated group is set by the model, the size of _t_ and _g_ reflects the model's assumptions rather than a property of manual work. The result did not depend on the larger Terraform sample: using only the first ten cycles gave a ratio of {R['h1_first10']['ratio']:.1f} and the same decision, and using only the push-triggered or only the dispatched cycles changes the Terraform mean by less than 3%."),
p(f"The simulated runs also show the built-in learning effect: build time fell with run order (Spearman's ρ = {R['sim_learning_rho']:.2f}, _p_ = {pv(R['sim_learning_p'])}), from {mn(R['sim_manual_runs'][0]['full_create_s'])} minutes in run 1 to {mn(R['sim_manual_runs'][-1]['full_create_s'])} minutes in run 10. Table 4.8 shows the sensitivity of the comparison to the key assumption, the median console time per resource. Even at 20 seconds per resource, the manual build would take {R['h1_sensitivity']['20']:.1f} minutes, {R['h1_sensitivity']['20'] / TFmin:.1f} times the Terraform build."),
caption("Table 4.8", "Sensitivity of the Simulated Manual Build Time to Console Time per Resource"),
table(["Console time per resource", "Manual build (min, SIMULATED)", f"Ratio to Terraform (measured {TFmin:.1f} min)"], sens_rows, [3000, 2800, 2840]),
note("Deterministic totals: 140 resources × time per resource + 8 minutes waiting, without rework or learning effect. The main simulation used 35 s."),
("fig", "fig4_4_manual_model.png", 6.2),
figcap("Figure 4.4. Left: measured Terraform build times (filled) and simulated manual build times (open). Right: simulated manual build time by run, showing the modelled learning effect. Manual values are SIMULATED."),
h3("4.8.2 Configuration Drift (H2)"),
p("H2 could not be tested. Only the production workspace existed during the measurement window; the pre-production workspace created in December 2025 had been destroyed and its state file held no resources, so there was no second environment against which to count differing attributes. Inspection of the code showed that environment-specific values are derived only from the workspace name, and a single variables file supplies the region to every stack."),
h3("4.8.3 Reproducibility (H3)"),
p(f"All {N} measured Terraform rebuilds completed with every service answering HTTP 200 (100%; Wilson 95% CI [{R['tf_rebuild_success']['low'] * 100:.1f}%, 100%]); with ten cycles the lower bound would have been 72.2%, so the larger sample tightens the reliability estimate considerably. In the simulation, {man['k']} of 10 manual rebuilds reproduced the baseline with no differing resource ({man['p'] * 100:.0f}%; 95% CI [{man['low'] * 100:.1f}%, {man['high'] * 100:.1f}%]). The difference was significant on the simulated data, Fisher's exact {pp(R['h3_fisher_p'])}. The model's expected manual success rate is {R['h3_p_success_model'] * 100:.0f}%; with a per-resource error probability of 0.2% it would be {R['h3_sensitivity']['0.002'] * 100:.0f}%, and with 1% it would be {R['h3_sensitivity']['0.01'] * 100:.0f}%."),
h3("4.8.4 Version-Control Coverage (H4)"),
p("Version-control coverage rose from 0% before the study to 79.2% of inventory components fully defined (87.5% including partial definitions). The proportion of infrastructure changes subject to peer review did not rise: no commit passed through a pull request. Because coverage is a census, no inferential test was applied."),
caption("Table 4.9", "Results of Hypothesis Testing"),
table(["H", "Relationship", "Result", "Statistic", "Decision"], [
    ["H1", "Method → provisioning duration", f"Terraform {TFmin:.1f} min (measured) vs. manual {mn(S['mean'])} min (simulated)", f"Welch p < .001; U = {H1['mw_U']:.0f}, p < .001", "Supported, conditional on the simulation"],
    ["H2", "Method → configuration drift", "One environment only", "None", "Not tested"],
    ["H3", "Method → reproducibility", f"{N}/{N} (measured) vs. {man['k']}/10 (simulated)", f"Fisher p {pv(R['h3_fisher_p']) if R['h3_fisher_p'] < .001 else '= ' + pv(R['h3_fisher_p'])}", "Supported, conditional on the simulation"],
    ["H4", "Pipeline integration → coverage and review", "Coverage 0% → 79.2%; peer review 0%", "Census", "Partially supported"],
    ["H5", "Depth moderates method → drift", "Drift not measured; one depth level observed", "None", "Not tested"],
], [500, 1900, 2500, 1840, 1900]),
h2("4.9 Pipeline Integration Depth (RQ3)"),
p("RQ3 asked whether pipeline integration depth moderates the effect of provisioning method on drift. The planned test was not possible for two reasons: drift could not be measured, and only one integration level was observed. The workflow ran Terraform automatically on every push to the main branch that changed one of three trigger scripts, recorded each run, and committed a report, which places it at level 2 of the framework (pipeline execution). It did not run a plan on pull requests or require approval before apply, so level 3 (gated apply) was not reached, and no run was made at level 1 for comparison. The repeat option added on 15 October increased the degree of automation, since sixteen cycles ran without a person starting each one, but it did not add a review gate and so did not change the level."),
h2("4.10 Summary of Quantitative Results"),
p(f"Terraform executed by GitHub Actions built the 140-resource environment from empty in a mean of {TFmin:.1f} minutes, with low variability, and destroyed it in {mn(G['Full destroy']['mean'])} minutes, most of which was spent destroying the five service stacks one after another. All {N} measured rebuilds and all {R['n_starts']} service start-ups succeeded, and the timings were stable across run order, day and hour of day; the only difference detected was an 18-second difference in build time between the two triggers. Against the simulated manual condition, Terraform was {H1['ratio']:.1f} times faster and more reproducible ({N}/{N} against {man['k']}/10); both differences were significant on the simulated data and robust to the sensitivity ranges tested. Version-control coverage rose to 79.2% while peer review remained absent. H2 and H5 were not tested."),
h2("4.11 Qualitative Findings (RQ4)"),
h3("4.11.1 Profile of the Implementation Record"),
p(f"Table 4.10 profiles the record analysed. The repository holds {REC['commits']} commits: {REC['human']} by the researcher and {REC['bot']} by the pipeline. They fall into two bursts: {REC['dec']} commits between 5 and 13 December 2025 (module development and architecture consolidation) and {REC['oct']} commits on 14 and 15 October 2026 (pipeline construction and the measurement campaign). Of the researcher's October commits, {REC['trigger_only']} did nothing but edit a trigger script to start a run. In all, {REC['skip_ci']} commit messages carry the marker that stops GitHub Actions from running, most of them run reports. The record was complemented by the {REC['run_reports']} run reports and the comments in the workflow and scripts."),
caption("Table 4.10", "Profile of the Implementation Record"),
table(["Source", "Period", "Volume", "Content"], [
    ["Git commits (development)", "5–13 Dec 2025", "20", "Module development; single API Gateway; single ALB; refactor; pre-production trial"],
    ["Git commits (pipeline and campaign)", "14–15 Oct 2026", f"{REC['oct']} ({REC['bot']} by pipeline; {REC['trigger_only']} trigger-only)", "Region move; workflow; reports; rebuild, redeploy and destroy modes; report fix; repeat option"],
    ["Run reports", "14–15 Oct 2026", str(REC['run_reports']), "Per-phase timeline and service health for runs 1, 2 and 4–32"],
    ["Script and workflow comments", "14–15 Oct 2026", "4 files", "Design rationale written into the code"],
], [2200, 1500, 1400, 3540]),
h3("4.11.2 Overview of Themes"),
p("Four themes were constructed (Table 4.11), presented in order of the weight they carry in explaining the quantitative results."),
caption("Table 4.11", "Thematic Structure of the Qualitative Findings"),
table(["Theme", "Subthemes", "Representative evidence"], [
    ["1. The architecture was found by rebuilding it", "Consolidation of load balancers and gateways; services added and removed; platform limits written into code", "\"Change to single api gateway\"; \"Stage 2: Change to Single ALB\"; \"Done - Single ALB but not rewrite\"; Inspector \"blocked by an SCP\""],
    ["2. State is the hardest part", "State files in Git; the bootstrap problem; preserving what must survive", "State files changed by thousands of lines per commit; state pulled before the bucket is deleted and pushed back after"],
    ["3. Destruction, not creation, is the bottleneck", "Sequential service-stack deletion; dependency order", f"{mn(G['Destroy deployments']['mean'])} minutes to destroy five service stacks in a loop; destroy order deployments → infrastructures → state"],
    ["4. Version control without review", "Direct pushes to main; uninformative messages; the pipeline as a trigger", f"{REC['human']} direct commits, 0 merges; messages \"Good\", \"Change\", \"Cleanup\"; {REC['trigger_only']} commits that only edit a trigger script"],
], [2300, 2900, 3440]),
h3("4.11.3 Theme 1: The Architecture Was Found by Rebuilding It"),
p("The architecture measured in October 2026 was not the one first written in December 2025. On the first day of development each service had its own API gateway; within half an hour of the initial commit this was replaced by one shared gateway (\"Change to single api gateway\"), and the following day the per-service load balancers were replaced by one shared load balancer with a target group and listener rule per service. The change was made in stages, recorded as \"Cleanup for multi ALB\", \"Stage 2: Change to Single ALB\", \"Done - Single ALB but not rewrite\" and finally \"Done - Single ALB + Multi Target Group for Multi Services\", and it touched every service stack. The set of services also moved: the authentication service was removed and later restored, and a sixth service (api1) was deleted from the deployments while its container repository remained in the shared stack. Platform limits were written into the code rather than worked around: the Inspector enabler carries the comment that it is \"blocked by an SCP on the AWS Free plan account\", and the certificate and domain resources are present but switched off."),
h3("4.11.4 Theme 2: State Is the Hardest Part"),
p("In December 2025 Terraform state was kept in local files that were committed to Git. Commits that changed one line of configuration routinely changed more than a thousand lines of state, as in \"Cleanup for multi ALB\" (over 2,400 lines in one state file). In October 2026 the service and infrastructure stacks moved to the S3 backend, but the stack that creates the S3 bucket cannot store its own state in that bucket, so its state remained a file in the repository. The pipeline therefore had to commit that file back after every rebuild, and the first attempt to do so failed: run 3 produced no report, and the next commit was \"Fix report push: commit remote-state state and autostash before rebase\". The rebuild script is shaped around state: its comments explain that the infrastructure state must be pulled before the state bucket is deleted (\"The state bucket is about to be deleted: keep the state that still tracks the ECR repos\") and pushed back after the bucket is recreated, and that a just-deleted bucket name \"can take a moment to become reusable\", which is why bucket creation is retried up to ten times."),
h3("4.11.5 Theme 3: Destruction, Not Creation, Is the Bottleneck"),
p(f"The run reports show that destroying the five service stacks took {mn(G['Destroy deployments']['mean'])} minutes on average, longer than the whole build. The rebuild script destroys the service stacks one after another in a loop, so their individual waits add up. Each stack contains an ECS service whose deletion must wait for running tasks to stop, while its other resources (alarms, scaling policies, routes) are simple to remove. The order of destruction is fixed by the dependencies the code expresses: services must go before the shared load balancer and network they attach to, and the shared stack before the state bucket that records it."),
h3("4.11.6 Theme 4: Version Control Without Review"),
p(f"Every change is in the repository, but none was reviewed. The history contains no merge commits; all {R['record']['human']} of the researcher's commits went straight to the main branch. Several messages say little about what changed or why: \"Good\", \"Change\" (twice), \"Cleanup\" and \"Done: Refactor\". In October 2026 the repository also became the pipeline's trigger: the workflow runs when one of three script files changes, and each script carries a line, \"Change note (edit to trigger a rebuild)\", whose only purpose is to be edited. Fifteen commits did exactly that, most with the default message \"Update rebuild.sh\". On 15 October the repetition itself was automated: a repeat option let each successful run start the next, so the last sixteen cycles needed one action rather than sixteen commits. The pipeline in turn writes its own commits, one per run, marked so that they do not trigger another run. The result is a complete history of what was applied and when, produced without any point at which a second person approved a change."),
h2("4.12 Integration of Quantitative and Qualitative Findings"),
p("Table 4.12 brings the two strands together for each research question."),
caption("Table 4.12", "Joint Display Integrating Quantitative and Qualitative Findings"),
table(["RQ / H", "Quantitative result", "Qualitative finding", "Meta-inference"], [
    ["RQ1", "Coverage 0% → 79.2% (87.5% with partial); 0% peer-reviewed", "Theme 4: everything committed, nothing reviewed; Theme 1: gaps are platform limits", "Complement: the file format delivered coverage; review did not follow automatically"],
    ["RQ2 / H1", f"Terraform {TFmin:.1f} min (measured) vs. manual {mn(S['mean'])} min (simulated)", "Theme 1: redesigns re-applied across five services quickly because they were code", "Converge, conditional on the simulation"],
    ["RQ2 / H3", f"{N}/{N} measured vs. {man['k']}/10 simulated", "Theme 2: reproducibility depended on careful state handling, including one failed report commit", "Complement: the rebuild was reliable because the state problem was engineered around"],
    ["RQ2 / H2", "Not measured", "Theme 2: pre-production workspace created then destroyed", "Gap: the evidence needed for H2 was not retained"],
    ["RQ3 / H5", "One depth level observed; no gate", "Theme 4: pipeline added automation but no review gate", "Diverge from the proposal: level 3 was never reached"],
    ["Destroy time (unplanned)", f"{mn(G['Full destroy']['mean'])} min to destroy; {R['destroy_deploy_share_pct']:.1f}% of the cycle in service stacks", "Theme 3: sequential deletion of service stacks", "Converge: the bottleneck is structural and fixable"],
], [1300, 2500, 2540, 2300], sz=18),
h2("4.13 Chapter Summary"),
p(f"This chapter reported {NW} measured Terraform rebuilds executed by GitHub Actions under two triggers on two days, {R['n_starts']} service start-ups, a 24-item component audit and a 152-resource inventory, compared with ten simulated manual console builds and rebuilds, together with a thematic analysis of the implementation record. The pipeline build was fast ({TFmin:.1f} minutes) and consistent, stable across run order, day and hour, and every rebuild succeeded. Conditional on the simulation, H1 and H3 were supported; H4 was partially supported; H2 and H5 could not be tested. Four themes explained these results: an architecture that converged through repeated rebuilding, state as the hardest engineering problem, destruction as the real bottleneck, and version control without review. Chapter 5 interprets these findings against the literature."),
]
