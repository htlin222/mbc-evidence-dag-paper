# Mbc Evidence Dag Paper

End-to-end reproducible study scaffold.

## Layout

```
analysis/         numbered analysis scripts (01_prepare_data.py -> ...)
data/raw/         raw downloads (gitignored)
data/processed/   harmonised inputs (gitignored, regenerable)
data/results/     analytic artefacts
docs/prereg.md    preregistration of primary + secondary outcomes
figures/          PDF + PNG figures
manuscript/       LaTeX sources, references.bib, compiled PDF
.github/workflows CI that rebuilds the PDF on each v* tag
```

## Reproduce

```bash
uv sync
uv run python analysis/01_prepare_data.py
uv run python analysis/02_<method>.py
uv run python analysis/03_<clinical>.py
uv run python analysis/04_figures.py
cd manuscript && make
```

## Preregistration

Before running any analysis against an outcome of interest, commit
`docs/prereg.md` with the primary hypothesis, pre-specified secondary
outcomes, and analysis plan. See the end-to-end-study skill
`preregistration-and-integrity.md` for the template.

## Licence
MIT. See `LICENSE`.
