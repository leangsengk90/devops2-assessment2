# Knowledge digest of `resources/`

Condensed from the 11 lecture decks and 2 dissertation templates in this folder so they don't have to be re-extracted. Many slides are image-only (diagrams, tables, examples); their content is missing from the extracted text, so treat this as the text content only.

## What's here

| File | What it is |
|---|---|
| `Week2 … Week14_*.pdf` | "IT Research Methodology" course slides by Chen Sov Ann (weeks 2, 3, 5, 7–14; weeks 1, 4, 6 absent) |
| `Dissertation_Complete_Chapters_1-6.docx` | University of Puthisastra (UP) full dissertation **template**: chapters 1–6, references, appendices A–K. All study content is `[PLACEHOLDER]` |
| `Dissertation_Template_Chapters_1-3_UP.docx` | Same template, proposal version: chapters 1–3 only (future tense, "Expected contribution" instead of Results/Conclusion in the abstract) |

No topic has been chosen yet in either template.

## The UP dissertation template

**Format rules**: APA 7th edition; Times New Roman 12 pt, 1.5 line spacing, 1.5" left margin (faculty rules take precedence); Khmer abstract may be required. Front matter: cover, Declaration of Originality (it names plagiarism, falsified data and **unacknowledged use of generative AI** as breaches), Supervisor's Approval, Acknowledgements, Abstract (Background / Aim / Methods / Results / Conclusion + keywords), TOC, lists of tables, figures, abbreviations.

**Default methodology built into the template**:
- Philosophy: pragmatism. Approach: abductive (deductive quant + inductive qual).
- Design: **explanatory sequential mixed methods** (Creswell & Plano Clark, 2018): Phase 1 cross-sectional survey → Phase 2 semi-structured interviews chosen from Phase 1 results → Phase 3 integration via a **joint display** (Fetters et al., 2013: building, connecting, merging).
- Theories offered: TAM (Davis 1989), UTAUT/UTAUT2 (Venkatesh 2003/2012), Diffusion of Innovations (Rogers 2003), TPB (Ajzen 1991). Pick one primary framework and extend it with one "proposed additional construct" (antecedent, mediator or moderator).
- Structure: 3 IVs + 1 additional construct → 1 DV; RQ1 = level of DV (descriptive), RQ2 = predictors, RQ3 = mediation/moderation, RQ4 = qualitative barriers/enablers; H1–H5.
- Sample size: larger of Krejcie & Morgan (95%, 5% margin) and G*Power (f² = .15, α = .05, power = .80), plus an attrition allowance; 12–20 interviews, stopping at saturation (3 consecutive interviews with no new codes).
- Instrument: 5-point Likert, items adapted from validated scales; forward–backward Khmer translation, cognitive pre-test, pilot n = 30.
- Quant analysis (SPSS / SmartPLS): screening (missing data, outliers ±3.29 / Mahalanobis, normality with skew/kurtosis within ±2, VIF), descriptives (mean ≤2.33 low, 2.34–3.66 moderate, ≥3.67 high), α and CR ≥ .70, AVE ≥ .50, Fornell–Larcker + HTMT < .85, Pearson r, regression or PLS-SEM, mediation by bootstrapping (5,000 resamples) or moderation by a mean-centred interaction term + simple slopes. Common method bias: Harman's test + full collinearity VIF < 3.3. f²: .02 small / .15 medium / .35 large.
- Qual analysis: reflexive thematic analysis, six phases (Braun & Clarke 2006, 2021); trustworthiness = credibility, transferability, dependability, confirmability (Lincoln & Guba 1985); COREQ reporting.
- Ethics: IRB approval, written consent (separate consent for audio recording), pseudonymised transcripts, encrypted storage, recruitment not done by supervisors.

**Chapter map**: 1 Introduction (background, problem, gap: contextual/theoretical/methodological, aim, objectives, RQs, hypotheses, significance, scope, key terms) · 2 Literature Review (strategy, theories, constructs, international → SE Asia → Cambodia evidence, comparison table of 8–12 studies, critical discussion, gap, framework + hypotheses) · 3 Methodology · 4 Results (report only, no interpretation) · 5 Discussion · 6 Conclusions & Recommendations (by objective; theoretical/practical/methodological/policy contributions).

**Appendix K — the template's own rules (examiners check these)**:
1. Replace placeholders consistently with Find & Replace; pick one option wherever there's a slash (`regression / PLS-SEM`).
2. The methodology and statistics references in the template are real and can be cited; every `[Author, Year]` must become a source you have actually read.
3. Chapter 4 = results only; interpretation belongs in Chapter 5.
4. Don't bury null or contradicting results; interpret them (the template's H3 is deliberately unsupported).
5. Every recommendation in Table 6.1 must cite the finding that supports it.
6. APA statistics: italic symbols, exact p to 3 decimals (p < .001 otherwise), an effect size with every test, no leading zero for values that can't exceed 1.
7. Check the chain: problem (1.2) → RQs (1.6) → gap (2.8 from 2.7) → Table 3.1 → results in Ch 4 → hypotheses in Tables 2.2 and 4.6 and Section 5.3 → a conclusion per objective (6.3).

## Course content by week

- **W2 Research methodology**: research = pose a question → collect data → present the answer; 6-step process (identify problem, review literature, specify purpose/RQs, collect data, analyse/interpret, report/evaluate); how quant and qual differ at each step; ethics (IRB, respectful data collection); features of good research (clear purpose, replicable procedure, honest reporting of errors, conclusions limited to what the data justify).
- **W3 Research problem**: definition (area of concern / condition to improve / troubling question); a good problem statement is factual, shows a gap, is interesting, researchable, noteworthy, feasible, ethical, challenging and clear; the "four Ps" (people, problem, phenomenon, programme); steps: broad area → sub-areas → pick one → RQs → objectives → assess → double-check; common errors (too narrow/vague, controversial, overdone, no cost or data consideration); quant problems explain or predict relations between variables, qual problems explore; a problem statement has five elements (the detail is image-only).
- **W5 Conceptualising a design**: design = plan, structure and strategy (Kerlinger, 1986); parameters: title, importance, literature survey, scope/objectives/problem, terminology, data selection/collection/analysis, results/interpretation, further research.
- **W7 Types of design**: experimental (random assignment, control of extraneous variables, manipulation, outcome measures, group comparison, threats to validity); correlational (explanatory vs prediction; direction/form/strength; scatter plots; partial correlation and multiple regression; 6 steps); survey (cross-sectional vs longitudinal; sampling, questionnaire/interview, instrument design, response rate).
- **W8 Quantitative data collection**: target vs accessible population; representative sample; sampling error; bigger samples mean less error, so use a formula; collection procedure (participants → permissions → information types → instruments → administer); instruments: questionnaires (open/closed questions; Likert 3/4/5/7-point, Thurstone, Osgood semantic differential with ≥5 bipolar pairs scored 1–7) and tests (achievement, aptitude, personal-social). Worked example: Cambodian teacher performance model, with job satisfaction mediating participatory decision-making (48 Likert items from DIA, TJSQ, Wang 2010).
- **W9 Quantitative analysis**: prepare (scoring, codebook, score types, software, input, clean) → descriptive (mean/median/mode, range/variance/SD, z-scores) → inferential (group comparison, relationships, regression/SEM/factor/path analysis, confidence intervals, effect sizes) → report (tables, figures, explanation) → interpret (summarise, explain, limitations, future research).
- **W10 Qualitative data collection**: forms (observations, interviews, documents, audio-visual); interview protocol; observation: site, gatekeeper, who and how long, observer role; protocol header + sketch + two columns (descriptive vs reflective notes); field issues.
- **W11 Qualitative analysis**: six steps (prepare/organise → code → describe and build themes → represent → interpret → validate); transcription; analysis by hand vs software (**QualCoder** is the tool demonstrated).
- **W12 Report and evaluation**: dissertation/thesis vs journal article vs conference paper; length (master's 50–100 pages); **proposal is written in future tense, final report in past tense** (a pilot is past tense even in a proposal); a proposal helps get permissions and sets quality criteria; writing practices (bias-reducing language, consistent point of view, connected parts, concise title).
- **W13 Article presentation**: tell a story (intro → data → summary → Q&A); most important point first; slides: few, titled, graphics over text, labelled axes, 20–24 pt type, no gimmicky animation; rehearse ≥6 times, time it, predict 3 likely questions; delivery (stand at 45°, don't block the screen, project your voice, avoid uptalk). A basic outline for a 10-minute talk is image-only.
- **W14 Plagiarism**: covers unattributed copying or paraphrasing, someone else rewriting or dictating your work, buying papers, and (at some schools) reusing your own paper; a first citation names the idea, the author, who the author is and the source; MLA vs APA vs Chicago examples; common knowledge (found in many sources, widely known, known before you researched it) needs no citation; opinions, data and disputable claims always do; "better to over-cite than under-cite".
