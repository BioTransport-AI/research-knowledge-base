# BioTransport AI research knowledge base

BioTransport AI (biotransportai.com, Pasadena CA) builds eye-photo health screening tools and is
raising external funding and sourcing training data for diabetes, anemia, glaucoma, and
cancer-imaging research. This repo holds the team's shared Claude Code skills and point-in-time
snapshots of the live research tracker. It is not the product codebase.

**On USC:** Dr. Penkova is USC faculty (Big Data in Biotransport Center), but BioTransport AI as a
company/brand is NOT formally integrated with USC. She looked into it and there was no clear
path. Per Dr. Penkova directly (Discord, 2026-09-22): **remove USC from every line of every
outreach email**, not just signatures, not just "USC-affiliated," all of it, including the NIH
email even though she signs that one as PI. This is a blanket rule now, not a judgment call: "If
we integrate one day and it works for us, then we can include the USC name." Every reference is
just "BioTransport AI" until she says otherwise.

## Team

- **Dr. Penkova**: PI / advisor
- **Noah**: researcher
- **Andy** (Jean-Tin Liew, given name; from Taiwan, studying in the US, goes by Andy/Anderson as
  his English name): researcher. External systems (Google Drive shares, Synapse registrations,
  etc.) will show "Jean-Tin Liew," not "Andy."

Primary coordination channel is Discord.

## Where things live

- **Live source of truth:** the "BioTransport AI Funding & Data Tracker" doc (a Claude Docs
  artifact, tabs: Funding & Data Tracker, Research Notes & Sources, Outreach Drafts, Free Data:
  Ready Now, Glaucoma Model) tracks funding leads, data sources, and meeting-notes-derived action
  items in real time. It's scoped to a Claude workspace, not this repo, so cloning this repo
  doesn't grant access to it. Ask whoever has access for the current link.
- **`tracker-snapshots/`**: dated PDF exports of that doc, committed periodically as a durable,
  offline-readable backup. These go stale between snapshots; treat the live doc as authoritative
  when both exist.
- **`datasets/`**: per-dataset README and fetch script for every source in the tracker's Free Data
  tab. No dataset files are ever committed here, for size and license reasons (see
  `datasets/README.md`). Scripts pull into a local, gitignored `data/` folder instead.
- **`papers/`**: reference papers the team is building on (e.g., the Parikh/Nguyen/Penkova 2026
  glaucoma paper). Fine to commit. These are either the team's own publications or copies shared
  for internal research use in a private repo, not bulk third-party datasets.
- **`brand/`**: logo concepts and reference images.
- **`.claude/skills/`**: Claude Code skills specific to BioTransport AI workflows. Currently:
  `biotransport-meeting-notes` (raw meeting notes turned into themed, actionable tracker updates),
  `biotransport-outreach-email` (research and draft outreach to funders/data providers), and
  `biotransport-data-workflow` (read-only-source, write-derived-output convention for working
  with the team's datasets, see `datasets/`).

## Standing rules

- **Confidentiality:** cancer-detection methodology (the specific DL/CV implementation) gets
  described publicly only at a high level, per Dr. Penkova, in this repo, the tracker doc, any
  paper draft, or grant narrative. Don't add implementation specifics beyond what's already been
  shared, even to fill in a plausible-sounding detail.
- **External outreach:** any email to an outside company or organization gets drafted, posted to
  Discord for Dr. Penkova's QC/sign-off, and only then sent, with her CC'd. Never send outreach
  unilaterally, and don't propose next steps that skip this.
- **Human-subjects data:** using existing public datasets (AI-READI, EyePACS, CP-AnemiC, TCIA,
  etc.) doesn't need new IRB review, since the original collectors already did that. Collecting
  new data from people (photos, readings, device tests) does. If in doubt, treat it as needing
  IRB review before proceeding.
