from pathlib import Path
from docxlib import h1, h2, h3, p, li, caption, table, note, ref

ROOT = Path(__file__).resolve().parent.parent

REFS = [
"Ajzen, I. (1991). The theory of planned behavior. _Organizational Behavior and Human Decision Processes, 50_(2), 179–211. https://doi.org/10.1016/0749-5978(91)90020-T",
"American Psychological Association. (2020). _Publication manual of the American Psychological Association_ (7th ed.). https://doi.org/10.1037/0000165-000",
"Begoug, M., Bessghaier, N., Ouni, A., AlOmar, E. A., & Mkaouer, M. W. (2023). What do infrastructure-as-code practitioners discuss: An empirical study on Stack Overflow. In _2023 ACM/IEEE International Symposium on Empirical Software Engineering and Measurement (ESEM)_ (pp. 1–12). IEEE. https://doi.org/10.1109/ESEM56168.2023.10304847",
"Begoug, M., Ouni, A., & Chouchen, M. (2025). How do infrastructure-as-code practitioners update their dependencies? An empirical study on Terraform module updates. In _2025 IEEE/ACM 22nd International Conference on Mining Software Repositories (MSR)_ (pp. 642–653). IEEE. https://doi.org/10.1109/MSR66628.2025.00100",
"Begoug, M., Ouni, A., & Khelifi, J. (2025). Understanding AWS provider dependency updates in infrastructure-as-code: Empirical study, taxonomy, and insights. _IEEE Transactions on Services Computing, 18_(6), 4318–4334. https://doi.org/10.1109/TSC.2025.3601051",
"Braun, V., & Clarke, V. (2006). Using thematic analysis in psychology. _Qualitative Research in Psychology, 3_(2), 77–101. https://doi.org/10.1191/1478088706qp063oa",
"Braun, V., & Clarke, V. (2021). One size fits all? What counts as quality practice in (reflexive) thematic analysis? _Qualitative Research in Psychology, 18_(3), 328–352. https://doi.org/10.1080/14780887.2020.1769238",
"Cohen, J. (1988). _Statistical power analysis for the behavioral sciences_ (2nd ed.). Lawrence Erlbaum Associates.",
"Creswell, J. W., & Plano Clark, V. L. (2018). _Designing and conducting mixed methods research_ (3rd ed.). SAGE Publications.",
"Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. _MIS Quarterly, 13_(3), 319–340. https://doi.org/10.2307/249008",
"Decan, A., Mens, T., Rostami Mazrae, P., & Golzadeh, M. (2022). On the use of GitHub Actions in software development repositories. In _2022 IEEE International Conference on Software Maintenance and Evolution (ICSME)_ (pp. 235–245). IEEE. https://doi.org/10.1109/ICSME55016.2022.00029",
"Fetters, M. D., Curry, L. A., & Creswell, J. W. (2013). Achieving integration in mixed methods designs: Principles and practices. _Health Services Research, 48_(6pt2), 2134–2156. https://doi.org/10.1111/1475-6773.12117",
"Field, A. (2018). _Discovering statistics using IBM SPSS Statistics_ (5th ed.). SAGE Publications.",
"Guba, E. G., & Lincoln, Y. S. (1994). Competing paradigms in qualitative research. In N. K. Denzin & Y. S. Lincoln (Eds.), _Handbook of qualitative research_ (pp. 105–117). SAGE Publications.",
"Guerriero, M., Garriga, M., Tamburri, D. A., & Palomba, F. (2019). Adoption, support, and challenges of infrastructure-as-code: Insights from industry. In _2019 IEEE International Conference on Software Maintenance and Evolution (ICSME)_ (pp. 580–589). IEEE. https://doi.org/10.1109/ICSME.2019.00092",
"Hedges, L. V. (1981). Distribution theory for Glass's estimator of effect size and related estimators. _Journal of Educational Statistics, 6_(2), 107–128. https://doi.org/10.3102/10769986006002107",
"Hilton, M., Tunnell, T., Huang, K., Marinov, D., & Dig, D. (2016). Usage, costs, and benefits of continuous integration in open-source projects. In _Proceedings of the 31st IEEE/ACM International Conference on Automated Software Engineering_ (pp. 426–437). ACM. https://doi.org/10.1145/2970276.2970358",
"Johnson, R. B., & Onwuegbuzie, A. J. (2004). Mixed methods research: A research paradigm whose time has come. _Educational Researcher, 33_(7), 14–26. https://doi.org/10.3102/0013189X033007014",
"Kinsman, T., Wessel, M., Gerosa, M. A., & Treude, C. (2021). How do software developers use GitHub Actions to automate their workflows? In _2021 IEEE/ACM 18th International Conference on Mining Software Repositories (MSR)_ (pp. 420–431). IEEE. https://doi.org/10.1109/MSR52588.2021.00054",
"Kolomytskyi, D., Rehida, P., Onyshko, O., & Ilchyshyna, Y. (2026). Generalized method for managing the lifecycle of Terraform infrastructure across multiple environments. _Computer Systems and Information Technologies_, (2), 26–32. https://doi.org/10.31891/csit-2026-2-3",
"Kumara, I., Garriga, M., Romeu, A. U., Di Nucci, D., Palomba, F., Tamburri, D. A., & van den Heuvel, W.-J. (2021). The do's and don'ts of infrastructure code: A systematic gray literature review. _Information and Software Technology, 137_, Article 106593. https://doi.org/10.1016/j.infsof.2021.106593",
"Leite, L., Rocha, C., Kon, F., Milojicic, D., & Meirelles, P. (2019). A survey of DevOps concepts and challenges. _ACM Computing Surveys, 52_(6), Article 127. https://doi.org/10.1145/3359981",
"Lincoln, Y. S., & Guba, E. G. (1985). _Naturalistic inquiry_. SAGE Publications.",
"Mann, H. B., & Whitney, D. R. (1947). On a test of whether one of two random variables is stochastically larger than the other. _The Annals of Mathematical Statistics, 18_(1), 50–60. https://doi.org/10.1214/aoms/1177730491",
"Nowell, L. S., Norris, J. M., White, D. E., & Moules, N. J. (2017). Thematic analysis: Striving to meet the trustworthiness criteria. _International Journal of Qualitative Methods, 16_(1), 1–13. https://doi.org/10.1177/1609406917733847",
"Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., Shamseer, L., Tetzlaff, J. M., Akl, E. A., Brennan, S. E., Chou, R., Glanville, J., Grimshaw, J. M., Hróbjartsson, A., Lalu, M. M., Li, T., Loder, E. W., Mayo-Wilson, E., McDonald, S., … Moher, D. (2021). The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. _BMJ, 372_, n71. https://doi.org/10.1136/bmj.n71",
"Podsakoff, P. M., MacKenzie, S. B., Lee, J.-Y., & Podsakoff, N. P. (2003). Common method biases in behavioral research: A critical review of the literature and recommended remedies. _Journal of Applied Psychology, 88_(5), 879–903. https://doi.org/10.1037/0021-9010.88.5.879",
"Rahman, A., Farhana, E., Parnin, C., & Williams, L. (2020). Gang of eight: A defect taxonomy for infrastructure as code scripts. In _Proceedings of the ACM/IEEE 42nd International Conference on Software Engineering_ (pp. 752–764). ACM. https://doi.org/10.1145/3377811.3380409",
"Rahman, A., Mahdavi-Hezaveh, R., & Williams, L. (2019). A systematic mapping study of infrastructure as code research. _Information and Software Technology, 108_, 65–77. https://doi.org/10.1016/j.infsof.2018.12.004",
"Rahman, A., Parnin, C., & Williams, L. (2019). The seven sins: Security smells in infrastructure as code scripts. In _2019 IEEE/ACM 41st International Conference on Software Engineering (ICSE)_ (pp. 164–175). IEEE. https://doi.org/10.1109/ICSE.2019.00033",
"Rahman, A., & Williams, L. (2019). Source code properties of defective infrastructure as code scripts. _Information and Software Technology, 112_, 148–163. https://doi.org/10.1016/j.infsof.2019.04.013",
"Regvart, D., Vlahović, I., & Balković, M. (2026). A controlled comparative evaluation of infrastructure as code tools: Deployment performance and maintainability across Terraform, Pulumi, and AWS CloudFormation. _Applied Sciences, 16_(6), Article 2971. https://doi.org/10.3390/app16062971",
"Rogers, E. M. (2003). _Diffusion of innovations_ (5th ed.). Free Press.",
"Rostami Mazrae, P., Mens, T., Golzadeh, M., & Decan, A. (2023). On the usage, co-usage and migration of CI/CD tools: A qualitative analysis. _Empirical Software Engineering, 28_(2), Article 52. https://doi.org/10.1007/s10664-022-10285-5",
"Saunders, M., Lewis, P., & Thornhill, A. (2019). _Research methods for business students_ (8th ed.). Pearson Education.",
"Shahin, M., Ali Babar, M., & Zhu, L. (2017). Continuous integration, delivery and deployment: A systematic review on approaches, tools, challenges and practices. _IEEE Access, 5_, 3909–3943. https://doi.org/10.1109/ACCESS.2017.2685629",
"Shapiro, S. S., & Wilk, M. B. (1965). An analysis of variance test for normality (complete samples). _Biometrika, 52_(3–4), 591–611. https://doi.org/10.1093/biomet/52.3-4.591",
"Vasilescu, B., Yu, Y., Wang, H., Devanbu, P., & Filkov, V. (2015). Quality and productivity outcomes relating to continuous integration in GitHub. In _Proceedings of the 2015 10th Joint Meeting on Foundations of Software Engineering_ (pp. 805–816). ACM. https://doi.org/10.1145/2786805.2786850",
"Venkatesh, V., Morris, M. G., Davis, G. B., & Davis, F. D. (2003). User acceptance of information technology: Toward a unified view. _MIS Quarterly, 27_(3), 425–478. https://doi.org/10.2307/30036540",
"Verdet, A., Hamdaqa, M., Da Silva, L., & Khomh, F. (2025). Assessing the adoption of security policies by developers in Terraform across different cloud providers. _Empirical Software Engineering, 30_(3), Article 74. https://doi.org/10.1007/s10664-024-10610-0",
"Villamizar, M., Garcés, O., Ochoa, L., Castro, H., Salamanca, L., Verano, M., Casallas, R., Gil, S., Valencia, C., Zambrano, A., & Lang, M. (2017). Cost comparison of running web applications in the cloud using monolithic, microservice, and AWS Lambda architectures. _Service Oriented Computing and Applications, 11_(2), 233–247. https://doi.org/10.1007/s11761-017-0208-y",
"Webster, J., & Watson, R. T. (2002). Analyzing the past to prepare for the future: Writing a literature review. _MIS Quarterly, 26_(2), xiii–xxiii.",
"Welch, B. L. (1947). The generalization of ‘Student’s’ problem when several different population variances are involved. _Biometrika, 34_(1–2), 28–35. https://doi.org/10.1093/biomet/34.1-2.28",
"Wilson, E. B. (1927). Probable inference, the law of succession, and statistical inference. _Journal of the American Statistical Association, 22_(158), 209–212. https://doi.org/10.1080/01621459.1927.10502953",
"Yin, R. K. (2018). _Case study research and applications: Design and methods_ (6th ed.). SAGE Publications.",
]

# commit log for Appendix B
_log = [l.split("|", 3) for l in (ROOT / "data" / "git-log.txt").read_text().splitlines()]
_n_timing = len((ROOT / "data" / "github-actions" / "timings.csv").read_text().splitlines()) - 1
_n_health = len((ROOT / "data" / "github-actions" / "service-health.csv").read_text().splitlines()) - 1
_codes = {
    "initial commit": "T1 initial architecture", "Change to single api gateway": "T1 consolidation",
    "Enhance API Gateway Routes and Integrations": "T1 consolidation; T2 state in Git",
    "Remove unnecessary .DS_Store files from the repository": "Housekeeping",
    "Good": "T4 uninformative message", "Remove auth service": "T1 service set changes",
    "Add Diagram and Cost Calculation": "Documentation", "Cleanup for multi ALB": "T1 consolidation; T2 state churn",
    "Stage 2: Change to Single ALB": "T1 staged redesign", "Done - Single ALB but not rewrite": "T1 staged redesign",
    "Done - Single ALB + Multi Target Group for Multi Services": "T1 staged redesign", "Change Diagram": "Documentation",
    "Done with Docs": "Documentation", "Cleanup": "T4 uninformative message", "Done: Refactor": "T1 refactor; T4 terse message",
    "Change for preprod": "T2 second environment", "Change": "T4 uninformative message",
    "Add resource URLs for GitHub repositories related to the project": "Documentation",
    "Move prod to ap-southeast-2 and add rebuild-prod workflow [skip ci]": "T1 platform constraint; T2 remote backend; T4 pipeline",
    "Update README.md": "Documentation", "Add per-run timeline report to rebuild-prod workflow [skip ci]": "T4 pipeline record",
    "Split pipeline into rebuild.sh and redeploy.sh triggers [skip ci]": "T4 trigger by editing scripts",
    "Update redeploy.sh": "T4 trigger by editing scripts", "Update rebuild.sh": "T4 trigger by editing scripts",
    "Fix report push: commit remote-state state and autostash before rebase": "T2 bootstrap state; T4 commit-push-wait",
    "Add destroy.sh: destroy all of prod including ECR images [skip ci]": "T3 destruction; T4 pipeline modes",
    "Update comment line number in rebuild.sh": "T4 trigger by editing scripts", "Modify change note in rebuild.sh": "T4 trigger by editing scripts",
    "Delete reports/rebuild-timings directory": "Housekeeping", "Delete DevOps2-Group4/project_timeline_02.png": "Housekeeping",
    "Delete DevOps2-Group4/project_timeline_01.png": "Housekeeping", "Delete DevOps2-Group4/Deploy Microservices.pdf": "Housekeeping",
    "Add repeat input to Rebuild prod workflow to chain runs": "T4 automated triggering (chained dispatch)",
}


def _code(msg):
    if msg.startswith("Prod "):
        return "T4 pipeline-authored record"
    if msg.startswith("feat(deployments)"):
        return "T1 service set changes"
    return _codes.get(msg, "")


APPX = [
h1("APPENDICES"),
h2("Appendix A: Component Inventory"),
p("The 24-item inventory used to measure version-control coverage (Section 4.4). Status: Full = defined and enabled in code; Partial = defined but switched off or incomplete; None = not in the repository."),
table(["Component", "Status", "Where defined / note"], [
    ["VPC; subnets; Internet Gateway; NAT gateways and Elastic IPs; route tables", "Full", "modules/vpc; main/infrastructures/network.tf"],
    ["Security groups and rules (ALB, ECS, VPC Link)", "Full", "modules/security-group; security-groups.tf"],
    ["ALB and HTTP listener", "Full", "main/infrastructures/alb.tf"],
    ["Target groups and listener rules", "Full", "modules/alb-target-group; each service main.tf"],
    ["ECS clusters; task definitions and Fargate services", "Full", "modules/ecs-cluster; modules/ecs-service"],
    ["Auto scaling targets and policies; CloudWatch alarms", "Full", "modules/ecs-service"],
    ["CloudWatch log groups", "Full", "modules/cloudwatch-log-group; cloudwatch.tf; api-gateway.tf"],
    ["ECR repositories and lifecycle policies", "Full", "modules/ecr; ecr-inspector.tf"],
    ["API Gateway, stage and VPC Link; routes and integrations", "Full", "api-gateway.tf; modules/api-gateway-route"],
    ["IAM roles and policies", "Full", "modules/iam-role; iam-roles.tf"],
    ["Terraform remote state (S3, DynamoDB)", "Full", "main/remote-state"],
    ["CI/CD pipeline definition", "Full", ".github/workflows/rebuild-prod.yml; rebuild.sh; redeploy.sh; destroy.sh"],
    ["Inspector scanning and alert topic", "Partial", "Enabler disabled: blocked by service control policy on the account plan"],
    ["TLS certificate binding and custom domain", "Partial", "Supported by module variables; not set; listener is HTTP"],
    ["Web Application Firewall", "None", "Not in repository"],
    ["Route 53 DNS records", "None", "Not in repository"],
    ["Branch protection and review rules", "None", "Repository setting; not configured"],
], [3700, 900, 4040], sz=18),
note("Rows group related inventory items; the 24 items are listed individually in Table 4.3."),
h2("Appendix B: Implementation Record"),
p("The complete commit history of the infrastructure repository analysed in Section 4.11, with the initial code assigned in the thematic analysis (T1–T4 refer to Themes 1–4)."),
table(["Date", "Commit", "Author", "Message", "Initial code"],
      [[d, h, ("pipeline" if "bot" in a else "researcher"), m, _code(m)] for d, h, a, m in _log],
      [1150, 900, 1050, 3540, 2000], sz=16),
note("Every commit to 15 October 2026 is listed, including the trigger commits and the pipeline's report commits for runs 1, 2 and 4–32. Run 3 left no report commit (Section 4.2)."),
h2("Appendix C: Measurement and Analysis Scripts"),
p("All scripts and raw data are held in the project repository and in the assessment2 folder submitted with this dissertation. Every figure in Chapter 4 can be regenerated by running analysis/analyze.py."),
table(["File", "Purpose"], [
    [".github/workflows/rebuild-prod.yml", "Pipeline: chooses rebuild, redeploy or destroy mode; runs the script; collects health; commits the report"],
    ["rebuild.sh; redeploy.sh; destroy.sh", "Pipeline procedures; rebuild preserves ECR repositories and state across deletion of the state bucket"],
    [".github/scripts/timeline.sh", "Phase timing helper (phase_begin / phase_end) writing to a CSV timeline"],
    [".github/scripts/report.py", "Writes per-run reports and the cumulative statistics table"],
    ["assessment2/data/simulated-manual/*", "SIMULATED manual runs (10 rows) and the model parameters with seed 20261015"],
    ["assessment2/data/github-actions/*.csv", f"Raw pipeline timings ({_n_timing} rows) and service health ({_n_health} rows)"],
    ["assessment2/analysis/analyze.py", "Manual-provisioning simulation (simulate_manual), all statistics and tests including the stability checks, Figures 4.1–4.4; writes results.json"],
    ["assessment2/data/git-log.txt", "The implementation record: every commit with date, author and message"],
], [3600, 5040], sz=18),
h2("Appendix D: Institutional Approval"),
p("[Insert the confirmation from the relevant University of Puthisastra committee that the study did not require ethical approval, and the written permission of the case organisation to use its architecture and to create an isolated AWS account for the study.]"),
h2("Appendix E: Research Timeline"),
p("The timeline as conducted is presented in Table 3.5. The proposal's planned twelve-week schedule (July to September 2026) is reproduced in the Assessment 1 submission."),
]


def appx_stats(gh_rows, sim_rows):
    cols = ["Destroy deployments", "Destroy infrastructures", "Destroy remote-state", "Create remote-state",
            "Create infrastructures", "Create deployments", "Wait until healthy", "Total cycle"]
    short = ["Destr. deploy", "Destr. infra", "Destr. state", "Create state", "Create infra", "Create deploy", "Healthy", "Total"]
    rows = [[f"Run {r['run_number']}"] + [str(r[c]) for c in cols] for r in gh_rows]
    return [
        h2("Appendix F: Statistical Output"),
        p("Per-cycle phase durations in seconds for every measured GitHub Actions rebuild, followed by the simulated manual runs. Descriptive statistics and test results are in Tables 4.4–4.9 and in analysis/results.json."),
        table(["Cycle"] + short, rows, [1000] + [955] * 8, sz=16),
        note("Measured. Run 2 was a redeploy; run 3 was excluded (Section 4.2)."),
        table(["Simulated run", "Hands-on (s)", "Waiting (s)", "Full build (s)", "Resources redone", "Differing resources on rebuild"],
              [[str(r["run"]), str(r["hands_on_s"]), str(r["wait_s"]), str(r["full_create_s"]), str(r["reworked_resources"]), str(r["rebuild_attr_errors"])] for r in sim_rows],
              [1300, 1400, 1300, 1400, 1500, 1740], sz=16),
        note("SIMULATED values (seed 20261015; parameters in Section 3.7.1 and data/simulated-manual/model_parameters.json)."),
        h2("Appendix G: Qualitative Codebook and Thematic Map"),
        table(["Code", "Definition", "Example entries", "Theme"], [
            ["Consolidation", "Merging per-service resources into shared ones", "Single API Gateway; single ALB in stages", "T1"],
            ["Service set changes", "Adding or removing a service stack", "Remove auth service; api1 removed, repository kept", "T1"],
            ["Platform constraint in code", "A limit of the account or platform recorded in code", "Inspector blocked by SCP; certificate variables unset", "T1"],
            ["State in Git", "Terraform state committed to version control", "Thousand-line state diffs in December commits", "T2"],
            ["Bootstrap state", "The stack that creates the backend cannot use it", "Remote-state file committed by pipeline; report fix", "T2"],
            ["Preserve across rebuild", "Keeping resources or state alive through destroy", "State pull/push; ECR import; targeted destroy", "T2"],
            ["Long deletion", "A resource whose deletion dominates a step", "ECS service \"Still destroying\" for about 3.5 minutes", "T3"],
            ["Ordering", "Destroy order fixed by dependencies", "Deployments → infrastructures → state", "T3"],
            ["Uninformative message", "Commit message that does not say what changed", "\"Good\", \"Change\", \"Cleanup\"", "T4"],
            ["Trigger by edit", "Editing a file solely to start the pipeline", "Change note lines in rebuild.sh", "T4"],
            ["Pipeline-authored record", "Commits written by the pipeline", "Prod rebuild report commits", "T4"],
            ["Automated triggering", "Removing the human edit from the trigger loop", "Repeat option; each run dispatches the next", "T4"],
        ], [1900, 2500, 2900, 1340], sz=18),
    ]
