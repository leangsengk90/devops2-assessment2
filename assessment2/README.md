# Assessment 2: Dissertation Completion and Presentation

| File | What it is |
|---|---|
| `KAO_Leangseng_ITRM_Assessment2_Dissertation.docx` | Full dissertation, Chapters 1–6, built on `resources/Dissertation_Complete_Chapters_1-6.docx` |
| `KAO_Leangseng_ITRM_Assessment2_Presentation.pptx` | 15-slide presentation covering every required topic (slide 10: stability over 30 runs) |
| `data/github-actions/` | Measured: 30 GitHub Actions rebuilds and 1 redeploy (14–15 Oct 2026), copied unmodified from `reports/github-actions/` |
| `data/git-log.txt` | The implementation record: all 78 commits to 15 Oct 2026 (`git log --reverse`) |
| `data/simulated-manual/` | **Simulated** manual console runs (seed 20261015) and the model parameters |
| `data/git-log.txt` | The 30-commit implementation record |
| `analysis/analyze.py` | Computes every statistic and Figures 4.1–4.4 and writes `results.json` |
| `figures/` | All figures used in the dissertation |
| `build/` | Scripts that generate the .docx (`build.py`) and the .pptx (`deck.js`) from the chapter text in `ch1.py`–`ch6.py` |

## Data integrity

- **Terraform condition:** measured. It comes only from the 30 GitHub Actions rebuilds: runs 1 and 4–16 were triggered by a push, runs 17–32 by a chained `workflow_dispatch` (repeat option). Run 3 left no report and is excluded. Section 4.6 tests whether the trigger, day, run order or hour of day affected the timings. Local CLI runs are not used.
- **Missing value:** in run 14 the finance service has no steady-state timestamp (it answered HTTP 200); it is treated as missing, not as a failure.
- **Manual condition:** **simulated** by `simulate_manual()` in `analysis/analyze.py`. The parameters are stated in Section 3.7.1, the seed is fixed so anyone can regenerate the values, and a sensitivity analysis is in Table 4.8 and Section 4.8.3. The dissertation labels these values as simulated wherever they appear, and H1/H3 are reported as "supported, conditional on the simulation".
- **Not tested:** H2 and H5, because only one environment existed.

## Before you submit

1. **PDF:** export the .docx to PDF from Word (File > Save As > PDF) after accepting the field update.
2. **Appendix D:** insert the ethics confirmation and the organisation's permission letter.
3. **AI statement:** check that the acknowledgement of generative AI use on the Acknowledgements page matches what you did. The declaration requires it.
4. **Table of contents:** when Word asks to update fields on opening, choose Yes so the page numbers refresh.
5. **Unverified figures:** the Regvart et al. (2026) per-tool timings and the Rostami Mazrae et al. (2023) "13 of 22" figure come from your own reading notes. They could not be re-checked online because the full texts were blocked.

## Rebuilding

```
python analysis/analyze.py   # needs pandas, scipy, matplotlib
python build/figs.py
python build/slide_figs.py   # chart images for slides 9 and 11
python build/build.py        # needs python-docx
node build/deck.js           # needs pptxgenjs
```
