# Zenodo DOI Setup — 15 minutes total

You need a Zenodo DOI for the data/code availability statement in both papers.
The cleanest path is the **GitHub → Zenodo webhook**, which mints a DOI
automatically every time you push a git tag.

## One-time setup (5 minutes)

1. Sign in to **https://zenodo.org** using your GitHub account (top-right "Log in with GitHub").
2. Visit **https://zenodo.org/account/settings/github/**.
3. Find the row for `mbc-evidence-dag-paper` in your repo list. Toggle the switch to **ON**. (If the repo isn't listed, click "Sync" first.)
4. Zenodo is now watching the repo for new release tags.

## Push the existing v3.0.0 tag to GitHub (3 minutes)

If you haven't created the GitHub remote yet:
```bash
# replace <your-github-username> with your actual GitHub handle
gh repo create <your-github-username>/mbc-evidence-dag-paper --public \
  --description "Pre-registered graph-theoretic framework for evidence-free decision points in mBC + NSCLC guideline trees" \
  --homepage "https://medrxiv.org/content/10.1101/<DOI-TBD>"
git remote add origin git@github.com:<your-github-username>/mbc-evidence-dag-paper.git
```

Then push everything including tags:
```bash
git push -u origin main
git push origin --tags
```

## Trigger Zenodo deposit (2 minutes)

The GitHub→Zenodo webhook will see the push of `v3.0.0` and:

1. Create a snapshot of the entire repo at that tag.
2. Mint a Zenodo DOI in the format `10.5281/zenodo.XXXXXXX`.
3. Show the DOI on https://zenodo.org/account/settings/github/ within ~5 minutes.

## Edit the Zenodo metadata (3 minutes)

Once Zenodo creates the deposit:

1. Visit your Zenodo dashboard → find the new deposit → "Edit"
2. Set fields:

| Field | Value |
|---|---|
| Resource type | Software |
| Title | mbc-evidence-dag-paper: graph-theoretic framework for guideline–trial evidence concordance |
| Description | A pre-registered, reproducible computational framework for measuring evidence-free decision points in clinical-guideline decision trees, applied across HR+/HER2- breast cancer and EGFR/ALK NSCLC. Tagged release v3.0.0. |
| Keywords | research synthesis methods; clinical guideline evaluation; graph theory; LLM-based extraction; oncology |
| License | MIT |
| Version | v3.0.0 |
| ORCID | [FILL IN your ORCID] |

3. Click "Publish" to finalize the DOI.

## Use the DOI in both papers

Once you have `10.5281/zenodo.XXXXXXX`, replace the placeholder in:

- `manuscript/paper_A_clinical_v3.tex` line ~166 (Data availability statement)
- `manuscript/paper_B_methods_v3.tex` line ~165 (Data Availability Statement)
- `release/submission_kit_paperB_medrxiv/medrxiv_metadata.md` (Data Availability)

Then recompile both papers (`latexmk -pdf -cd manuscript/paper_A_clinical_v3.tex`, same for B).

## medRxiv expects the Zenodo DOI BEFORE preprint submission

Order of operations:
1. Push v3.0.0 to GitHub (this minute)
2. Wait for Zenodo to mint the DOI (~5 min)
3. Update both papers with the real Zenodo DOI
4. Recompile both papers
5. Submit Paper B to medRxiv

You can technically submit to medRxiv with "DOI pending" but it's cleaner to have the real DOI in the preprint when it goes live.
