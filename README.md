# BioTransport AI Research Knowledge Base

The shared knowledge base behind BioTransport AI's research work.

## What this is for

The team works with Claude (an AI research assistant) throughout the week: taking meeting notes, researching funding and data sources, drafting outreach, and now building the first prediction models. This repository is what gives Claude a consistent, accurate memory to work from.

Without it, every conversation with Claude would start from scratch. With it, Claude can look up what the team already knows: the papers the team is building on, notes from past meetings, and the public research datasets the team has chosen to use, instead of guessing or asking the same questions twice.

This repository is a knowledge base for the team's AI tools, not a software product itself. The actual diabetes, anemia, and glaucoma screening models live in their own separate repositories (see "Related repositories" below).

## What is inside

- **papers**: the published research papers the team's models are based on, including the Parikh, Nguyen, and Penkova 2026 glaucoma paper.
- **datasets**: information about every public research dataset the team is using or considering, plus scripts that automatically download and organize them. The dataset files themselves are never stored here. They are too large, and some come with licenses that do not allow it. The scripts simply pull them from the original source onto whoever's computer needs them. See `datasets/README.md` for more.
- **tracker-snapshots**: saved copies of the team's live funding and data tracker document, kept here as a backup. The live, editable version is the one the team actually works from day to day (ask Noah or Dr. Penkova for the link).
- **brand**: logo and visual identity files.
- **.claude**: instructions that tell Claude how to do specific BioTransport AI tasks, like turning meeting notes into tracker updates or drafting outreach emails. You will not usually need to open this folder.

## How the team works day to day

The live tracker document (funding leads, data sources, meeting notes, and action items) is a separate, shared document, not a file in this repository. This repository keeps periodic backups of it and the materials around it. Most day to day coordination happens in Discord.

## Related repositories

- [glaucoma-model](https://github.com/BioTransport-AI/glaucoma-model): the glaucoma detection model itself, including code, the training data pipeline, and results. This is where the research engineering actually happens.

More repositories will likely be added here as work on diabetes and anemia screening begins.

## Getting started

1. Clone this repository.
2. Open it in Claude Code. The skills in `.claude/skills` load automatically, so Claude already knows how to help with BioTransport AI tasks.
3. Read `CLAUDE.md` for full team context and the standing rules Claude follows in this repository.

## Team

Dr. Penkova (PI), Noah, and Andy, coordinating primarily through Discord.
