// Assessment 2 presentation. Run from a directory where pptxgenjs is installed:
//   NODE_PATH=<dir>/node_modules node deck.js
const pptxgen = require("pptxgenjs");
const path = require("path");
const R = require("../analysis/results.json");

const OUT = path.join(__dirname, "..", "KAO_Leangseng_ITRM_Assessment2_Presentation.pptx");
const FIG = path.join(__dirname, "..", "figures");
const DARK = "221B35", PURPLE = "6A4FA0", ORANGE = "E39A3B", CARD = "F1F0F7", INK = "1E1A2B", MUTED = "6B6680", WHITE = "FFFFFF";
const HEAD = "Cambria", BODY = "Calibri";
const N = 15;

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "KAO LEANGSENG";
pres.title = "Evaluating the Effectiveness of Terraform and GitHub Actions for AWS Infrastructure Automation";
pres.theme = { headFontFace: HEAD, bodyFontFace: BODY };

pres.defineSlideMaster({
  title: "CONTENT", background: { color: WHITE },
  objects: [{ placeholder: { options: { name: "title", type: "title", x: 0.45, y: 0.42, w: 9.1, h: 0.62, fontFace: HEAD, fontSize: 28, bold: true, color: DARK, valign: "middle", align: "left", margin: 0 }, text: "" } }],
});
pres.defineSlideMaster({ title: "DARK", background: { color: DARK } });

const T = (s, text, o) => s.addText(text, Object.assign({ isTextBox: true, fontFace: BODY, color: INK, margin: 0 }, o));

function content(n, title) {
  const s = pres.addSlide({ masterName: "CONTENT" });
  s.addText(title, { placeholder: "title" });
  T(s, [{ text: String(n).padStart(2, "0"), options: { color: ORANGE, bold: true } }, { text: `  /  ${N}`, options: { color: MUTED } }],
    { x: 0.45, y: 0.18, w: 1.5, h: 0.25, fontSize: 10, objectName: "page" });
  return s;
}

function card(s, x, y, w, h, big, label, sub, name) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: CARD }, line: { color: CARD }, rectRadius: 0.08, objectName: name + "-card" });
  T(s, big, { x: x + 0.18, y: y + 0.1, w: w - 0.3, h: 0.55, fontFace: HEAD, fontSize: 28, bold: true, color: PURPLE, objectName: name + "-num" });
  T(s, label, { x: x + 0.18, y: y + 0.66, w: w - 0.3, h: 0.28, fontSize: 13, bold: true, objectName: name + "-label" });
  if (sub) T(s, sub, { x: x + 0.18, y: y + 0.93, w: w - 0.3, h: 0.3, fontSize: 10.5, italic: true, color: MUTED, objectName: name + "-sub" });
}

function dot(s, x, y, num, name) {
  s.addShape(pres.shapes.OVAL, { x, y, w: 0.34, h: 0.34, fill: { color: PURPLE }, line: { color: PURPLE }, objectName: name });
  if (num !== undefined) T(s, String(num), { x, y, w: 0.34, h: 0.34, fontSize: 12, bold: true, color: WHITE, align: "center", valign: "middle", objectName: name + "-n" });
}

function rows(s, items, x, y, w, gap, name) {
  items.forEach(([head, sub], i) => {
    dot(s, x, y + i * gap + 0.03, i + 1, `${name}-dot${i}`);
    T(s, head, { x: x + 0.48, y: y + i * gap, w, h: 0.27, fontSize: 14, bold: true, objectName: `${name}-h${i}` });
    T(s, sub, { x: x + 0.48, y: y + i * gap + 0.27, w, h: 0.42, fontSize: 11.5, color: MUTED, valign: "top", objectName: `${name}-s${i}` });
  });
}

function darkPanel(s, x, y, w, h, heading, lines, name) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: DARK }, line: { color: DARK }, rectRadius: 0.08, objectName: name });
  T(s, heading, { x: x + 0.25, y: y + 0.18, w: w - 0.5, h: 0.28, fontSize: 12, bold: true, color: ORANGE, objectName: name + "-head" });
  T(s, lines.map((l, i) => ({ text: l, options: { bullet: true, breakLine: i < lines.length - 1 } })),
    { x: x + 0.25, y: y + 0.5, w: w - 0.5, h: h - 0.65, fontSize: 12, color: WHITE, valign: "top", paraSpaceAfter: 5, objectName: name + "-body" });
}

const m = (s) => (s / 60).toFixed(1);
const NT = R.n_tf, C = R.campaign, REC = R.record, PC = R.gh_phases["Full create"], TRG = R.trigger["Full create"], F10 = R.first10["Full create"];

// 1 Title -------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "DARK" });
  s.addShape(pres.shapes.OVAL, { x: 7.6, y: -1.2, w: 3.6, h: 3.6, fill: { color: "34294F" }, line: { color: "34294F" }, objectName: "circle-1" });
  s.addShape(pres.shapes.OVAL, { x: 8.6, y: 3.3, w: 2.4, h: 2.4, fill: { color: "34294F" }, line: { color: "34294F" }, objectName: "circle-2" });
  T(s, "MASTER OF SCIENCE IN INFORMATION TECHNOLOGY  ·  ASSESSMENT 2", { x: 0.45, y: 0.6, w: 7, h: 0.25, fontSize: 9, bold: true, color: ORANGE });
  T(s, "Evaluating the Effectiveness of Terraform and GitHub Actions for AWS Infrastructure Automation",
    { x: 0.45, y: 0.95, w: 7.6, h: 1.65, fontFace: HEAD, fontSize: 30, bold: true, color: WHITE, valign: "top", objectName: "title" });
  T(s, "Terraform on GitHub Actions (measured) vs manual AWS console (simulated)", { x: 0.45, y: 2.7, w: 7.4, h: 0.3, fontSize: 13, italic: true, color: "C9C2E0" });
  T(s, [{ text: "Kao Leangseng", options: { bold: true, color: WHITE, breakLine: true } },
        { text: "Student ID: UPS240590", options: { color: "C9C2E0", breakLine: true } },
        { text: "Supervisor: Dr. Chen Sovann", options: { color: "C9C2E0" } }],
    { x: 0.45, y: 3.3, w: 5, h: 0.85, fontSize: 13, paraSpaceAfter: 4 });
  T(s, "Faculty of Science and Technology  ·  University of Puthisastra  ·  October 2026", { x: 0.45, y: 4.65, w: 7, h: 0.3, fontSize: 11, color: "A79FC4" });
  s.addNotes("Introduce the study: it measured what changes when an AWS architecture moves from hand-built to Terraform run through GitHub Actions.");
}

// 2 Topic and background ---------------------------------------------------------
{
  const s = content(2, "Research Topic and Background");
  T(s, "Cloud infrastructure can be built from code, but many teams still build it by hand.", { x: 0.45, y: 1.12, w: 9.1, h: 0.35, fontSize: 15, italic: true, color: PURPLE });
  rows(s, [
    ["Infrastructure as Code (IaC)", "A file describes the network, load balancer and services; a tool such as Terraform makes AWS match it."],
    ["CI/CD pipelines", "GitHub Actions already builds and ships application code automatically in most teams."],
    ["The split pipeline", "Application delivery is automated, but the environment it runs on is still changed through the console."],
    ["Why Cambodia", "Banks supervised by the National Bank of Cambodia need auditable change. No local IaC evidence exists."],
  ], 0.45, 1.65, 4.6, 0.85, "bg");
  card(s, 6.0, 1.65, 3.5, 1.25, "253 s", "Terraform build in prior work", "Regvart et al. (2026), smaller architecture", "c1");
  card(s, 6.0, 3.05, 3.5, 1.25, "43.9%", "of active repos use GitHub Actions", "Decan et al. (2022), 69,147 repositories", "c2");
  s.addNotes("Background: IaC and CI/CD matured separately; organisations often automate the app first.");
}

// 3 Problem ---------------------------------------------------------------------
{
  const s = content(3, "Research Problem");
  T(s, "The pipeline automated the application. The AWS environment it deployed into was created and changed by hand.", { x: 0.45, y: 1.12, w: 9.1, h: 0.5, fontSize: 15, italic: true, color: PURPLE });
  const probs = [["No audit trail", "Nobody can see who changed the network, load balancer or IAM, when, or why."],
                 ["Environments drift", "Development, staging and production slowly stop matching."],
                 ["Rebuilds depend on memory", "Recovery or a new region relies on what engineers remember."]];
  probs.forEach(([h, t], i) => {
    const x = 0.45 + i * 3.07;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.85, w: 2.87, h: 1.75, fill: { color: CARD }, line: { color: CARD }, rectRadius: 0.08, objectName: `p${i}` });
    dot(s, x + 0.2, 2.03, i + 1, `pd${i}`);
    T(s, h, { x: x + 0.2, y: 2.47, w: 2.5, h: 0.3, fontSize: 14, bold: true });
    T(s, t, { x: x + 0.2, y: 2.8, w: 2.5, h: 0.7, fontSize: 11.5, color: MUTED, valign: "top" });
  });
  darkPanel(s, 0.45, 3.85, 9.1, 1.25, "THE CONTESTED QUESTION", [
    "Not whether this is a problem, but how much fixing it with Terraform actually changes, and at what cost.",
    "Prior studies compare Terraform with other tools, never with the manual work it replaces."], "pp");
  s.addNotes("State the problem and why it needs measurement in a specific setting.");
}

// 4 Aim, objectives, RQs -------------------------------------------------------------
{
  const s = content(4, "Aim, Objectives and Research Questions");
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.45, y: 1.15, w: 9.1, h: 0.75, fill: { color: CARD }, line: { color: CARD }, rectRadius: 0.08, objectName: "aim" });
  T(s, [{ text: "AIM  ", options: { bold: true, color: ORANGE } }, { text: "Build the AWS architecture in Terraform, run it through GitHub Actions, measure four outcomes against manual provisioning, and explain what made the change hard." }],
    { x: 0.65, y: 1.2, w: 8.7, h: 0.65, fontSize: 13, valign: "middle" });
  T(s, "OBJECTIVES", { x: 0.45, y: 2.1, w: 4, h: 0.25, fontSize: 11, bold: true, color: MUTED });
  T(s, ["Document how the architecture is provisioned", "Build a modular Terraform codebase", "Integrate it into GitHub Actions",
        "Measure duration, drift, reproducibility, coverage", "Explain barriers; recommend"].map((t, i, a) => ({ text: t, options: { bullet: { type: "number" }, breakLine: i < a.length - 1 } })),
    { x: 0.45, y: 2.4, w: 4.3, h: 2.6, fontSize: 13, valign: "top", paraSpaceAfter: 6 });
  T(s, "RESEARCH QUESTIONS", { x: 5.1, y: 2.1, w: 4, h: 0.25, fontSize: 11, bold: true, color: MUTED });
  const rq = [["RQ1", "How is it provisioned, and how much is under version control?"],
              ["RQ2", "How does Terraform differ from manual work on the four outcomes?"],
              ["RQ3", "Does pipeline integration depth moderate drift?"],
              ["RQ4", "What barriers and enablers arise in practice?"]];
  rq.forEach(([k, t], i) => {
    T(s, k, { x: 5.1, y: 2.42 + i * 0.64, w: 0.55, h: 0.3, fontSize: 13, bold: true, color: PURPLE });
    T(s, t, { x: 5.7, y: 2.42 + i * 0.64, w: 3.85, h: 0.55, fontSize: 12.5, valign: "top" });
  });
  s.addNotes("Five objectives, four research questions; RQ1-3 quantitative, RQ4 qualitative.");
}

// 5 Literature and gap ---------------------------------------------------------------
{
  const s = content(5, "Key Literature and Research Gap");
  T(s, "20 peer-reviewed studies reviewed, every DOI verified", { x: 0.45, y: 1.12, w: 9.1, h: 0.3, fontSize: 14, italic: true, color: PURPLE });
  const lit = [["IaC tool performance", "Regvart et al. (2026): Terraform 253 s vs CloudFormation 623 s; no failures in 30 cycles"],
               ["IaC quality and security", "Verdet et al. (2025): encryption neglected in 812 projects; Rahman et al. (2019, 2020): smells, defects"],
               ["Dependency maintenance", "Begoug et al. (2025): module lag about 10 months; AWS provider lag about 9 months"],
               ["CI/CD and GitHub Actions", "Hilton et al. (2016); Kinsman et al. (2021); Rostami Mazrae et al. (2023): migration to GitHub Actions"]];
  lit.forEach(([h, t], i) => {
    T(s, h, { x: 0.45, y: 1.6 + i * 0.85, w: 4.6, h: 0.28, fontSize: 13.5, bold: true });
    T(s, t, { x: 0.45, y: 1.88 + i * 0.85, w: 4.6, h: 0.5, fontSize: 11, color: MUTED, valign: "top" });
  });
  darkPanel(s, 5.35, 1.6, 4.2, 3.35, "THREE GAPS", [
    "Empirical: no study measures Terraform against manual provisioning of the same system",
    "Theoretical: IaC and the pipeline are studied apart, so the effect of review is never isolated",
    "Contextual: no IaC evidence from Cambodia or a regulated setting"], "gap");
  s.addNotes("Summarise the four strands of literature and the three gaps.");
}

// 6 Framework and hypotheses -------------------------------------------------------
{
  const s = content(6, "Conceptual Framework and Hypotheses");
  s.addImage({ path: path.join(FIG, "fig2_1_framework.png"), x: 0.45, y: 1.15, w: 5.6, h: 3.26, objectName: "framework" });
  const hs = [["H1", "Terraform is faster to provision"], ["H2", "Terraform reduces drift between environments"],
              ["H3", "Terraform rebuilds succeed more often"], ["H4", "Pipeline raises version-control and review coverage"],
              ["H5", "Integration depth moderates the drift effect"]];
  hs.forEach(([k, t], i) => {
    T(s, k, { x: 6.35, y: 1.25 + i * 0.66, w: 0.5, h: 0.3, fontSize: 13, bold: true, color: PURPLE });
    T(s, t, { x: 6.85, y: 1.25 + i * 0.66, w: 2.7, h: 0.55, fontSize: 12, valign: "top" });
  });
  T(s, "Grounded in IaC principles, the deployment pipeline concept and DevOps outcome measurement; acceptance models (TAM, UTAUT) set aside because the outcomes are system properties.",
    { x: 0.45, y: 4.6, w: 9.1, h: 0.45, fontSize: 10.5, italic: true, color: MUTED });
}

// 7 Methodology ----------------------------------------------------------------------
{
  const s = content(7, "Research Methodology");
  const blocks = [["PHILOSOPHY", "Pragmatism"], ["APPROACH", "Abductive"], ["DESIGN", "Explanatory sequential mixed methods"], ["SETTING", "Isolated AWS account, one region"]];
  blocks.forEach(([k, v], i) => {
    const x = 0.45 + i * 2.31;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.15, w: 2.13, h: 0.95, fill: { color: CARD }, line: { color: CARD }, rectRadius: 0.08, objectName: `m${i}` });
    T(s, k, { x: x + 0.15, y: 1.25, w: 1.9, h: 0.25, fontSize: 10, bold: true, color: ORANGE });
    T(s, v, { x: x + 0.15, y: 1.5, w: 1.9, h: 0.55, fontSize: 13, bold: true, valign: "top" });
  });
  s.addImage({ path: path.join(FIG, "fig3_1_design.png"), x: 0.45, y: 2.3, w: 5.0, h: 2.67, objectName: "design" });
  darkPanel(s, 5.75, 2.3, 3.8, 2.67, "NO HUMAN PARTICIPANTS", [
    "Outcomes are machine-recorded, not self-reported",
    `Qualitative data: the real implementation record (${REC.commits} commits, ${REC.run_reports} run reports, logs)`,
    "Ethics: confidentiality, no live data, credential handling, cost control"], "meth");
}

// 8 Data collection and analysis -------------------------------------------------------
{
  const s = content(8, "Data Collection and Analysis");
  card(s, 0.45, 1.15, 2.13, 1.28, String(NT), "pipeline rebuilds", "GitHub Actions, measured", "d1");
  card(s, 2.76, 1.15, 2.13, 1.28, "10", "manual builds", "SIMULATED, seeded model", "d2");
  card(s, 5.07, 1.15, 2.13, 1.28, "152", "AWS resources", "140 rebuilt every cycle", "d3");
  card(s, 7.38, 1.15, 2.17, 1.28, "24", "inventory items", "coverage audit", "d4");
  T(s, "PLANNED VS ACHIEVED", { x: 0.45, y: 2.65, w: 4, h: 0.25, fontSize: 11, bold: true, color: MUTED });
  s.addTable([
    [{ text: "Measure", options: { bold: true, fill: { color: CARD } } }, { text: "Planned", options: { bold: true, fill: { color: CARD } } }, { text: "Achieved", options: { bold: true, fill: { color: CARD } } }],
    ["Terraform cycles", "30", `${NT} (${C.push} + ${C.dispatch} chained)`], ["Manual runs", "10 observed", "10 simulated"], ["Environments for drift", "3", "1"], ["Integration depth levels", "3", "1"],
  ], { x: 0.45, y: 2.95, w: 4.7, colW: [1.7, 0.9, 2.1], fontFace: BODY, fontSize: 11, color: INK, border: { type: "solid", pt: 0.5, color: "D9D6E5" }, rowH: 0.36, objectName: "planned" });
  darkPanel(s, 5.45, 2.65, 4.1, 2.8, "ANALYSIS", [
    "Descriptives, CV, Shapiro–Wilk, Tukey outliers",
    "Stability: trigger, day, run order, hour of day",
    "Welch t + Mann–Whitney U; Hedges' g",
    "Fisher's exact test for rebuild success",
    "Manual condition SIMULATED: stated parameters, fixed seed, sensitivity analysis",
    "Reflexive thematic analysis; joint display"], "an");
  s.addNotes(`Be explicit: manual runs were not observed; the baseline is a model and labelled as such. The planned 30 Terraform cycles were achieved: ${C.push} were triggered by a commit and ${C.dispatch} by a chained workflow_dispatch, ${REC.run_reports} run reports in total including the redeploy. Every pipeline run destroys and recreates 140 of the 152 resources; ECR repositories are kept.`);
}

// 9 Findings: speed and reliability --------------------------------------------------------
{
  const s = content(9, "Findings 1: Terraform Pipeline Results (Measured)");
  const pc = R.gh_phases["Full create"], pd = R.gh_phases["Full destroy"];
  card(s, 0.45, 1.15, 2.2, 1.28, `${m(pc.mean)} min`, "to build from empty", `SD ${pc.sd.toFixed(0)} s · CV ${pc.cv_pct.toFixed(1)}% · n = ${NT}`, "f1");
  card(s, 0.45, 2.53, 2.2, 1.28, `${m(pd.mean)} min`, "to destroy", `service stacks = ${R.destroy_deploy_share_pct.toFixed(1)}% of cycle`, "f2");
  card(s, 0.45, 3.91, 2.2, 1.28, `${NT} / ${NT}`, "rebuilds succeeded", `${R.http_200} / ${R.n_http} HTTP 200`, "f3");
  s.addImage({ path: path.join(FIG, "slide_phases.png"), x: 2.85, y: 1.12, w: 6.7, h: 2.42, objectName: "phase-chart" });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 2.85, y: 3.7, w: 6.7, h: 1.49, fill: { color: CARD }, line: { color: CARD }, rectRadius: 0.08, objectName: "read-card" });
  T(s, "HOW TO READ IT", { x: 3.05, y: 3.8, w: 3, h: 0.22, fontSize: 9.5, bold: true, color: ORANGE });
  T(s, [
    `Removing takes longer than building: ${m(pd.mean)} min vs ${m(pc.mean)} min. The five service stacks alone take ${m(R.gh_phases["Destroy deployments"].mean)} min.`,
    `The stacks are destroyed one after another, about ${(R.destroy_deploy_per_service_s / 60).toFixed(1)} min each, so this one step sets the cycle length.`,
    `Short whiskers = consistent runs: each phase varies by seconds, not minutes (build SD ${pc.sd.toFixed(0)} s).`,
  ].map((t, i, a) => ({ text: t, options: { bullet: true, breakLine: i < a.length - 1 } })),
    { x: 3.05, y: 4.06, w: 6.35, h: 1.08, fontSize: 10.5, color: INK, valign: "top", paraSpaceAfter: 2, objectName: "read-body" });
  s.addNotes(`All values on this slide are measured from the GitHub Actions pipeline over ${NT} rebuilds. Building from empty took ${m(pc.mean)} minutes (95% CI ${m(pc.ci_low)}–${m(pc.ci_high)}); destroying took ${m(pd.mean)} minutes; a whole cycle about ${m(R.gh_phases["Total cycle"].mean)} minutes. Destruction, not creation, dominates: the five service stacks are destroyed one after another, about ${(R.destroy_deploy_per_service_s / 60).toFixed(1)} minutes each. Services reached steady state in ${R.health.mean.toFixed(0)} s on average; one finance start-up in run 14 has no steady-state timestamp but answered HTTP 200.`);
}

// 10 Findings: stability over 30 runs ---------------------------------------------------------
{
  const s = content(10, "Findings 2: Stable Across 30 Runs (Measured)");
  s.addImage({ path: path.join(FIG, "fig4_2_run_order.png"), x: 0.45, y: 1.05, w: 5.4, h: 2.41, objectName: "run-order" });
  T(s, "Blue: triggered by a push (n = " + C.push + ")  ·  Orange: chained workflow_dispatch (n = " + C.dispatch + ")  ·  bands = mean ± 2 SD",
    { x: 0.45, y: 3.48, w: 5.75, h: 0.25, fontSize: 9, italic: true, color: MUTED });
  const hdr = (t) => ({ text: t, options: { bold: true, fill: { color: CARD } } });
  const f = (x) => x < .001 ? "< .001" : x.toFixed(3).replace(/^0/, "");
  s.addTable([
    [hdr("Check (full build)"), hdr("Result"), hdr("p")],
    ["Trend over run order", `ρ = ${R.trend["Full create"].rho.toFixed(2)}`, f(R.trend["Full create"].p)],
    ["Hour of day", `ρ = ${R.hour["Full create"].rho.toFixed(2)}`, f(R.hour["Full create"].p)],
    ["14 Oct vs 15 Oct", `${m(R.by_day["Full create"].day1.mean)} vs ${m(R.by_day["Full create"].day2.mean)} min`, f(R.by_day["Full create"].test.welch_p)],
    ["Push vs dispatch", `${m(TRG.push.mean)} vs ${m(TRG.dispatch.mean)} min`, f(TRG.test.welch_p)],
    ["Push vs dispatch, total cycle", `${m(R.trigger["Total cycle"].push.mean)} vs ${m(R.trigger["Total cycle"].dispatch.mean)} min`, f(R.trigger["Total cycle"].test.welch_p)],
  ], { x: 0.45, y: 3.78, w: 5.75, colW: [2.45, 2.4, 0.9], fontFace: BODY, fontSize: 9.5, color: INK, border: { type: "solid", pt: 0.5, color: "D9D6E5" }, rowH: 0.25, margin: [2, 5, 2, 5], objectName: "stab" });
  darkPanel(s, 6.45, 1.1, 3.1, 4.05, "WHAT 30 RUNS ADD", [
    `No trend: run 1 is the only cycle outside the band`,
    `95% CI of the build narrowed from ±${((F10.ci_high - F10.ci_low) / 2).toFixed(0)} s (10 runs) to ±${((PC.ci_high - PC.ci_low) / 2).toFixed(0)} s`,
    `Chained runs built ${(TRG.dispatch.mean - TRG.push.mean).toFixed(0)} s (${((TRG.test.ratio - 1) * 100).toFixed(1)}%) slower; destroy and total cycle did not differ`,
    `Likely cloud-side conditions, not the trigger: same steps, and the day effect alone was not significant`,
    `Success rate 30/30: lower 95% bound ${(R.tf_rebuild_success.low * 100).toFixed(0)}% (was 72% with 10)`], "stab-panel");
  s.addNotes(`Thirty cycles ran over two days: ${C.push} triggered by editing rebuild.sh and pushing, then ${C.dispatch} chained by a repeat option in which each run started the next. ` +
    `The pipeline steps were identical. Durations show no trend with run order or hour of day. The only difference detected: the back-to-back dispatched runs built about ${(TRG.dispatch.mean - TRG.push.mean).toFixed(0)} seconds slower ` +
    `(Welch p = ${f(TRG.test.welch_p)}), while destroy and the total cycle did not differ. The day comparison points the same way but is not significant, so the most plausible explanation is AWS and runner conditions during the back-to-back runs. ` +
    `It is tiny next to the H1 gap, so the 30 cycles were pooled. Thirty cycles also match Regvart et al. (2026), so the variability comparison is like for like.`);
}

// 11 Findings: Terraform vs manual -------------------------------------------------------
{
  const s = content(11, "Findings 3: Terraform vs Manual Console");
  const tf = +(R.gh_phases["Full create"].mean / 60).toFixed(1), man = +(R.sim_manual.mean / 60).toFixed(1);
  s.addImage({ path: path.join(FIG, "slide_h1.png"), x: 0.6, y: 1.05, w: 3.9, h: 2.97, objectName: "h1-chart" });
  T(s, `${R.h1.ratio.toFixed(1)}× faster · Welch t(${R.h1.welch_df.toFixed(1)}) = ${R.h1.welch_t.toFixed(1)}, p < .001 · rebuilds identical ${NT}/${NT} vs ${R.man_rebuild_success.k}/10 (Fisher p ${R.h3_fisher_p < .001 ? "< .001" : "= " + R.h3_fisher_p.toFixed(3).replace(/^0/, "")})`,
    { x: 0.45, y: 4.1, w: 4.3, h: 0.5, fontSize: 10.5, color: INK, valign: "top" });
  T(s, "Manual values are SIMULATED from a stated, seeded model; results hold from 20 s to 120 s per resource.", { x: 0.45, y: 4.6, w: 4.3, h: 0.45, fontSize: 10, italic: true, color: MUTED, valign: "top" });
  const hdr = (t) => ({ text: t, options: { bold: true, fill: { color: CARD } } });
  s.addTable([
    [hdr("H"), hdr("Result"), hdr("Decision")],
    ["H1 Duration", `${tf} vs ${man} min (simulated)`, "Supported*"],
    ["H2 Drift", "Only one environment", "Not tested"],
    ["H3 Reproducibility", `${NT}/${NT} vs ${R.man_rebuild_success.k}/10 (simulated)`, "Supported*"],
    ["H4 Coverage & review", `Coverage 0% → 79.2%; review 0 of ${REC.human}`, "Partially supported"],
    ["H5 Depth × drift", "Drift not measured", "Not tested"],
  ], { x: 5.0, y: 1.15, w: 4.55, colW: [1.45, 1.9, 1.2], fontFace: BODY, fontSize: 10.5, color: INK, border: { type: "solid", pt: 0.5, color: "D9D6E5" }, rowH: 0.5, valign: "middle", objectName: "hyp" });
  T(s, "* conditional on the simulated manual condition", { x: 5.0, y: 4.35, w: 4.55, h: 0.3, fontSize: 10, italic: true, color: MUTED });
  s.addNotes(`Be explicit that the manual condition is simulated: Terraform is measured over ${NT} cycles, the manual side comes from a published, seeded model of 10 builds. The ratio is ${R.h1.ratio.toFixed(1)}; with only the first ten Terraform cycles it was ${R.h1_first10.ratio.toFixed(1)}, so the extra runs do not change the decision. Even at 20 s per resource in the console, a manual build would take ${R.h1_sensitivity["20"].toFixed(0)} minutes.`);
}

// 11 Findings: themes --------------------------------------------------------------------
{
  const s = content(12, "Findings 4: Why It Was Hard (RQ4)");
  const th = [["The architecture was found by rebuilding it", "Per-service load balancers and gateways merged in stages; easy because it was code"],
              ["State is the hardest part", "State files in Git; the bucket that holds state can't hold its own; rebuild built around it"],
              ["Destruction, not creation, is the bottleneck", `Destroying the five service stacks takes ${m(R.gh_phases["Destroy deployments"].mean)} minutes, one after another`],
              ["Version control without review", `${REC.human} direct commits, none reviewed; ${REC.trigger_only} only edited a script to start a run`]];
  th.forEach(([h, t], i) => {
    const x = 0.45 + (i % 2) * 4.65, y = 1.2 + Math.floor(i / 2) * 1.85;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 4.45, h: 1.65, fill: { color: CARD }, line: { color: CARD }, rectRadius: 0.08, objectName: `t${i}` });
    dot(s, x + 0.22, y + 0.22, i + 1, `td${i}`);
    T(s, h, { x: x + 0.7, y: y + 0.2, w: 3.55, h: 0.55, fontSize: 14, bold: true, valign: "top" });
    T(s, t, { x: x + 0.7, y: y + 0.8, w: 3.55, h: 0.75, fontSize: 11.5, color: MUTED, valign: "top" });
  });
  s.addNotes(`Themes from reflexive thematic analysis of ${REC.commits} commits (${REC.human} by the researcher, ${REC.bot} by the pipeline), ${REC.run_reports} run reports and the pipeline code. Theme 4 grew during the campaign: ${REC.trigger_only} commits existed only to trigger a run, and when that became tedious the answer was more automation (a repeat option chaining 16 runs), not review.`);
}

// 12 Contributions and recommendations ------------------------------------------------------
{
  const s = content(13, "Main Contributions and Recommendations");
  rows(s, [
    ["Theoretical", "Code and review are separable: coverage reached 79% while review stayed at 0%"],
    ["Practical", `Reusable modules and rebuild procedure; measured ${m(PC.mean)} min to build, ${m(R.gh_phases["Full destroy"].mean)} min to remove, over ${NT} runs`],
    ["Methodological", "Mixed methods on an engineering artefact, using the commit history as qualitative data"],
    ["Policy", "For regulated Cambodian institutions, require a code history and a review record"],
  ], 0.45, 1.2, 4.3, 0.92, "con");
  darkPanel(s, 5.45, 1.2, 4.1, 3.85, "TOP RECOMMENDATIONS", [
    "Plan on pull request; approve before apply; protect main",
    "Short-lived OIDC credentials instead of access keys",
    "Destroy service stacks in parallel",
    "Create the state bucket once, outside the rebuild",
    "Pin provider versions and commit the lock file",
    "Codify TLS, WAF and DNS; keep two environments with drift checks"], "rec");
}

// 13 Timeline ----------------------------------------------------------------------------
{
  const s = content(14, "Research Timeline");
  const tl = [["Dec 2025", "Build", "Terraform modules; shared ALB and API Gateway"], ["Aug 2026", "Proposal", "Chapters 1–3 (Assessment 1)"],
              ["14 Oct 2026", "Build + Phase 1", "Pipeline; 10 rebuilds and 1 redeploy (push)"], ["15 Oct 2026", "Phase 1", "20 rebuilds: 4 push, 16 chained"],
              ["Oct 2026", "Phases 2–3", "Analysis, themes, joint display, writing"]];
  s.addShape(pres.shapes.LINE, { x: 0.8, y: 2.55, w: 8.4, h: 0, line: { color: "C9C2E0", width: 2 }, objectName: "axis" });
  tl.forEach(([d, ph, t], i) => {
    const x = 0.45 + i * 1.84;
    dot(s, x + 0.2, 2.38, i + 1, `tl${i}`);
    T(s, d, { x, y: 1.55, w: 1.7, h: 0.3, fontSize: 13, bold: true, color: PURPLE });
    T(s, ph, { x, y: 1.88, w: 1.7, h: 0.3, fontSize: 11, bold: true, color: ORANGE });
    T(s, t, { x, y: 2.95, w: 1.7, h: 1.0, fontSize: 11.5, color: INK, valign: "top" });
  });
  T(s, "The proposal planned 12 weeks from July to September 2026; measurement slipped to October 2026, when all 30 planned cycles were run in two days.", { x: 0.45, y: 4.5, w: 9.1, h: 0.35, fontSize: 11, italic: true, color: MUTED });
}

// 14 References --------------------------------------------------------------------------
{
  const s = content(15, "References");
  const refs = [
    "Begoug, M., Ouni, A., & Chouchen, M. (2025). How do infrastructure-as-code practitioners update their dependencies? MSR 2025, 642–653. https://doi.org/10.1109/MSR66628.2025.00100",
    "Braun, V., & Clarke, V. (2021). One size fits all? Qualitative Research in Psychology, 18(3), 328–352. https://doi.org/10.1080/14780887.2020.1769238",
    "Creswell, J. W., & Plano Clark, V. L. (2018). Designing and conducting mixed methods research (3rd ed.). SAGE.",
    "Decan, A., Mens, T., Rostami Mazrae, P., & Golzadeh, M. (2022). On the use of GitHub Actions in software development repositories. ICSME 2022, 235–245. https://doi.org/10.1109/ICSME55016.2022.00029",
    "Hilton, M., et al. (2016). Usage, costs, and benefits of continuous integration in open-source projects. ASE 2016, 426–437. https://doi.org/10.1145/2970276.2970358",
    "Rahman, A., Farhana, E., Parnin, C., & Williams, L. (2020). Gang of eight: A defect taxonomy for infrastructure as code scripts. ICSE 2020, 752–764. https://doi.org/10.1145/3377811.3380409",
    "Regvart, D., Vlahović, I., & Balković, M. (2026). A controlled comparative evaluation of infrastructure as code tools. Applied Sciences, 16(6), 2971. https://doi.org/10.3390/app16062971",
    "Rostami Mazrae, P., Mens, T., Golzadeh, M., & Decan, A. (2023). On the usage, co-usage and migration of CI/CD tools. Empirical Software Engineering, 28(2), 52. https://doi.org/10.1007/s10664-022-10285-5",
    "Verdet, A., Hamdaqa, M., Da Silva, L., & Khomh, F. (2025). Assessing the adoption of security policies by developers in Terraform. Empirical Software Engineering, 30(3), 74. https://doi.org/10.1007/s10664-024-10610-0",
    "Full list of 44 references (APA 7th) in the dissertation.",
  ];
  T(s, refs.map((r, i) => ({ text: r, options: { breakLine: i < refs.length - 1, italic: i === refs.length - 1, color: i === refs.length - 1 ? MUTED : INK } })),
    { x: 0.45, y: 1.12, w: 9.1, h: 4.1, fontSize: 9.5, valign: "top", paraSpaceAfter: 4 });
}

pres.writeFile({ fileName: OUT }).then(() => console.log("saved", OUT));
