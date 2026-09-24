# AI-READI

**Condition:** Diabetes · **Modality:** Multimodal — retinal imaging + clinical/tabular data
**Source:** [FAIRhub](https://fairhub.io/) / [aireadi.org](https://aireadi.org/)
**Size:** ~4,000 participants, 350k+ files, ~3.8TB for the full release — by far the largest
dataset in this list. This alone is reason enough it can never live in this git repo.

## No fetch script — by design, not an oversight

Access requires logging in, stating a research purpose, and attesting to proper data usage before
each release's public tier unlocks; the controlled tier (full demographic/race-ethnicity data)
needs a separate request reviewed by AI-READI's Data Access Committee. This is a deliberate
human-in-the-loop gate for a dataset with real participant-privacy stakes — not something to
script around even if it were technically possible.

1. Go to [fairhub.io](https://fairhub.io/), create an account, and complete the public-tier access
   flow.
2. For the controlled tier, follow the request process on the same site (see the outreach draft
   already sent to their Data Access Committee — Outreach Drafts tab, email 6).
3. Download into `data/ai-readi-diabetes/` once access is granted. Given the size, consider
   downloading only the modalities actually needed first rather than the full release.
