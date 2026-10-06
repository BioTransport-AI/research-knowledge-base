# BioTransport AI Research Knowledge Base

The shared knowledge base behind BioTransport AI's research work.

## Purpose

The team works throughout the week: taking meeting notes, researching funding and data sources, drafting outreach, and developing models. This repository is a knowledge base of that contextual work, and is what gives AI agents a consistent, accurate memory to work from. Without this knowledge base, every query to a language model or internet search starts from scratch. With this repo localized to your machine, an AI agent can look up what the team already knows: the papers, notes from previous research meetings, and the public research datasets we chose to use.

*Note:* This repository is a knowledge base for the team's AI tools, and **is not** a Biotransport AI software product itself. The real screening models (diabetes, anemia, cancer, glaucoma) live in their own separate repositories (see "Related repositories" below).

## Contents

- **papers**: the published research papers the team's models are based on, including the Parikh, Nguyen, and Penkova 2026 glaucoma paper.
- **datasets**: information about every public research dataset the team is using or considering, plus scripts that automatically download and organize them. The dataset files themselves are never stored here. They are too large, and some come with licenses that do not allow it. The scripts pull them from the source onto your local machine. See `datasets/README.md` for more.
- **tracker-snapshots**: saved copies of the team's live funding and data tracker document, kept here as a backup.
- **brand**: logo and visual identity files for historical reference and ease of redesign.
- **.claude**: instructions tailored for Claude agents on how to act on BioTransport AI tasks, like turning meeting notes into tracker updates or drafting outreach emails. You probably will not need to open this folder.

## How to develop this Repo

Periodic updates (after approved Pull Requests) with respect to work completed, meetings held, and important key info tracked. Backups of it and the materials around it are traceable and easily maintained. Most of the context comes from day-to-day coordination in Discord and Zoom meetings.

## Related repositories

- [glaucoma-model](https://github.com/BioTransport-AI/glaucoma-model): the glaucoma detection model itself, including code, the training data pipeline, and results. This is where the research engineering actually happens.

More repositories will likely be added here as work on diabetes and anemia screening begins.

## Getting started (Example)

1. Clone this repository.
2. If using Claude Code, the skills in `.claude/skills` load automatically, so your AI agent already knows how to help with granular BioTransport AI tasks with the core context as ground truth.
3. Read `CLAUDE.md` for full team context and the standing rules Claude follows in this repository.

## Team

Dr. Penkova (PI), Noah, and Andy.
