import json
from pathlib import Path
from docxlib import h1, h2, h3, p, li, caption, table, note

R = json.loads((Path(__file__).resolve().parent.parent / "analysis" / "results.json").read_text())
N = R["n_tf"]
G = R["gh_phases"]
TF = G["Full create"]["mean"] / 60
DES = G["Full destroy"]["mean"] / 60
MAN = R["sim_manual"]["mean"] / 60
K = R["man_rebuild_success"]["k"]
REC = R["record"]
TRG = R["trigger"]["Full create"]

BLOCKS = [
h1("CHAPTER 6: CONCLUSIONS AND RECOMMENDATIONS"),
h2("6.1 Introduction"),
p("This chapter summarises the study, states the conclusions reached against each objective, sets out the study's contributions, makes recommendations that are each traceable to a finding, acknowledges the limitations, and identifies directions for future research."),
h2("6.2 Summary of the Study"),
p(f"The study set out to establish what a Terraform-based, pipeline-integrated approach changes when an AWS architecture is provisioned, and what makes the change difficult. A modular Terraform codebase was built for a five-service containerised architecture of 152 managed resources, run through GitHub Actions, and measured over thirty complete destroy-and-rebuild cycles on two days, the number the proposal planned. Manual creation of the same architecture in the AWS console was represented by a stated, seeded simulation of ten builds and ten rebuilds. A component audit measured version-control coverage, and the implementation record of {REC['commits']} commits, {REC['run_reports']} run reports and the pipeline code was analysed thematically. Of the five hypotheses, H1 and H3 were supported conditional on the simulated manual condition, H4 was partially supported, and H2 and H5 could not be tested."),
h2("6.3 Conclusions by Research Objective"),
h3("6.3.1 Objective 1: Current Provisioning and Version-Control Coverage"),
p("Before the study the architecture was provisioned entirely by hand and nothing was under version control. After the study 19 of 24 components (79.2%) were fully defined in code and 2 more partially. The components left outside were those that depend on something outside the code: a certificate and domain, a firewall, DNS records and repository review rules. Every infrastructure change was recorded, but none was reviewed."),
h3("6.3.2 Objective 2: A Modular Terraform Codebase"),
p("A modular codebase of fifteen reusable modules and seven root stacks (remote state, shared infrastructure and five services) was built, with an S3 backend and DynamoDB locking for all but the stack that creates them. It provisioned the full architecture identically in every cycle. The codebase supports multiple environments through workspaces, but only one environment was maintained during the study."),
h3("6.3.3 Objective 3: Pipeline Integration"),
p("A GitHub Actions workflow was built that can rebuild, redeploy or destroy the environment, times every phase, checks service health and commits a report after every run. It reached integration depth level 2: automated execution with a shared record, but no plan review or approval gate. The gated level proposed in the framework was not implemented."),
h3("6.3.4 Objective 4: Measured Outcomes"),
p(f"Terraform executed by GitHub Actions built the environment from empty in {TF:.1f} minutes on average, with a coefficient of variation below 5%, and destroyed it in {DES:.1f} minutes. All {N} rebuilds and all {R['n_starts']} service start-ups succeeded, and the timings showed no trend over run order, day or hour; the only difference detected was that back-to-back dispatched runs built about {TRG['dispatch']['mean'] - TRG['push']['mean']:.0f} seconds slower. Against the simulated manual condition the build was {R['h1']['ratio']:.1f} times faster ({TF:.1f} against {MAN:.1f} minutes) and more reproducible ({N} of {N} rebuilds against {K} of 10), both significant on the simulated data and robust across the sensitivity ranges tested; these comparisons are conditional on the simulation. Drift could not be measured."),
h3("6.3.5 Objective 5: Barriers, Enablers and Recommendations"),
p("The main enabler was that the architecture could be redesigned and re-applied cheaply because it was code. The main barriers were managing Terraform state (in particular the stack that creates the state bucket), the time taken to destroy ECS services sequentially, the commit-push-wait loop of developing a workflow that cannot be run locally, and the absence of any review step. The technical barriers were overcome by one engineer within days; the governance barrier was not addressed. Recommendations follow in Section 6.5."),
h2("6.4 Contributions of the Study"),
h3("6.4.1 Theoretical Contribution"),
p("The study separates two things that the IaC literature usually treats as one: putting infrastructure into code, and forcing changes to that code through review. It shows empirically that the first can be achieved almost completely while the second does not happen at all, which supports treating pipeline integration depth, and review in particular, as a construct in its own right. It also proposes destruction duration as an outcome measure that the literature has underweighted."),
h3("6.4.2 Practical Contribution"),
p("The study provides a working module structure, a rebuild procedure that preserves container images and state across the deletion of the state bucket, and measured figures that an engineering team can plan with: about 8 minutes to build this class of architecture through a pipeline, about 20 minutes to remove it, and about 1.5 minutes for a Fargate service to become healthy. These figures give a realistic basis for decisions about disposable test environments and recovery rehearsals."),
h3("6.4.3 Methodological Contribution"),
p("The study shows how an explanatory sequential mixed methods design can be applied to an engineering artefact, using machine-recorded timings for the quantitative strand and the version-control history as a qualitative record that was not written for the study. The timing and reporting scripts are reusable, and the use of two independent timing implementations allowed a check on measurement procedure that exposed the effect of a separate planning step."),
h3("6.4.4 Policy Contribution"),
p("For a Cambodian financial institution, the study supplies the first local evidence that infrastructure can be brought under version control quickly, and a warning that version control is not the same as approved change. Supervisory expectations for controlled change management are met by the combination of a code history and a review record, not by the history alone."),
h2("6.5 Recommendations"),
p("Table 6.1 lists each recommendation with the party responsible and the finding that supports it. The subsections that follow group them by audience."),
caption("Table 6.1", "Recommendations, Responsible Parties and Supporting Evidence"),
table(["No.", "Recommendation", "Responsible party", "Supporting evidence"], [
    ["R1", "Run terraform plan on every pull request and require approval before apply on merge; protect the main branch", "Engineering team; platform manager", f"0 of {REC['human']} changes reviewed (Section 4.4); Theme 4"],
    ["R2", "Replace the long-lived access key with OpenID Connect short-lived credentials", "Engineering team", "Deviation in Section 3.11; Rahman, Parnin & Williams (2019)"],
    ["R3", "Destroy service stacks in parallel and scale services to zero before deletion", "Engineering team", "Service-stack destruction 64.6% of the cycle (Section 4.5); Theme 3"],
    ["R4", "Create the state bucket once, outside the rebuild cycle, and commit no state files", "Engineering team", "Theme 2; run 3 report failure"],
    ["R5", "Commit the dependency lock file, pin provider versions exactly and pin third-party actions to a commit", "Engineering team", "Provider constrained to a major version; lock file ignored (Table 5.1); Decan et al. (2022)"],
    ["R6", "Codify TLS, WAF and DNS so that security controls are under review", "Platform manager", "5 of 24 components not fully codified (Table 4.3)"],
    ["R7", "Maintain at least two environments and run scheduled drift detection", "Platform manager", "H2 untestable with one environment (Section 4.8.2)"],
    ["R8", "Accept code history together with review records as evidence of infrastructure change control", "Technology governance; regulator", "Coverage without review (Section 5.2)"],
    ["R9", "Reuse the measurement scripts and codebase in teaching cloud automation", "University of Puthisastra", "Reusable instruments (Section 6.4.3)"],
], [500, 3640, 1900, 2600]),
h3("6.5.1 Recommendations for Engineering Teams"),
p("Teams adopting Terraform should build the review gate at the same time as the pipeline, not afterwards (R1), because this study shows that a working pipeline removes the pressure to add one. Credentials should be short-lived from the start (R2). The rebuild procedure should destroy independent service stacks concurrently and drain services before deleting them (R3), which on the evidence here could remove most of the 18 minutes spent on sequential deletion, although that saving was not measured. The state bucket should be treated as long-lived infrastructure created once, so that no state file is ever committed (R4), and versions should be fixed exactly so that a rebuild in six months uses the same code (R5)."),
h3("6.5.2 Recommendations for Institutions and Platform Management"),
p("Platform managers should treat the uncodified components as the priority list for the next phase (R6), since edge security is exactly what an auditor will ask about, and should fund a second persistent environment with scheduled drift detection (R7). Without it, the claim that IaC keeps environments consistent cannot be checked."),
h3("6.5.3 Recommendations for Policymakers"),
p("Supervisors and internal governance functions assessing change management should ask for two things: the version history of the infrastructure code and the record of who approved each change (R8). This study shows that the first can exist in full without the second."),
h3("6.5.4 Recommendations for Educators and the University of Puthisastra"),
p("The scripts and Terraform code produced here can serve as a teaching artefact for cloud automation and for measuring engineering outcomes (R9). Courses should present state management and change review as core skills alongside writing Terraform, because those were where the difficulty lay."),
h2("6.6 Limitations of the Study"),
p("The study has six limitations. It is a single case: one architecture, one account, one region and one researcher, so its findings generalise analytically rather than statistically. The manual condition was simulated rather than observed, so H1 and H3 rest on a model whose parameters were the researcher's own. Only one environment existed, so drift, H2 and H5 were not tested. The gated level of integration depth was not implemented. Terraform reproducibility was measured by completion and service health rather than attribute by attribute. Finally, the researcher built, measured and interpreted the system, which bears most on the qualitative strand. The planned thirty cycles were achieved, but within two days and under two triggers, so they sample AWS and runner conditions over a short window; the small difference between the triggers shows that such conditions are visible in the data."),
h2("6.7 Recommendations for Future Research"),
p("Each limitation suggests a study. A timed manual baseline, ideally performed by several engineers following a written console procedure, would replace the simulated manual condition with observed data and test H1 and H3 directly. A study maintaining two or three environments over several months, with scheduled drift detection, would test H2. Implementing all three depth levels and comparing drift and policy violations across them would test H5 and check the result reported by Kolomytskyi et al. (2026). An attribute-level comparison of rebuilt environments would test reproducibility more strictly. A longitudinal follow-up would measure the maintenance cost that Begoug, Ouni, and Chouchen (2025) identify. Replication in other Cambodian organisations would test whether these findings transfer within the setting the study set out to inform."),
h2("6.8 Concluding Remarks"),
p("The question this study began with was whether moving an AWS architecture from hand-built to Terraform-managed is worth it. On the evidence here, the technical answer is yes, and quickly: within days one engineer had an environment that could be rebuilt identically in under ten minutes, every time. The harder answer concerns control. Code made every change visible, but it did not make anyone check a change before it took effect. For organisations in Cambodia's regulated sectors, the lesson is that the tool delivers the record and the organisation must still supply the review."),
]
