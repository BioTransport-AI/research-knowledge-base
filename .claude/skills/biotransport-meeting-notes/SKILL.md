---
name: biotransport-meeting-notes
description: Turn raw, stream-of-consciousness BioTransport AI meeting notes (Discord pastes, voice-to-text dumps, bullet fragments from Noah, Dr. Penkova, or Andy) into a clean, themed, actionable-steps summary and fold the results into the shared research tracker doc. Use this whenever someone pastes messy meeting notes, asks to "update the tracker with the meeting notes," mentions a recap with Dr. Penkova or Andy, or hands over fragmented notes that need organizing into next steps — even if they don't name this skill directly.
---

# BioTransport AI meeting notes → tracker update

BioTransport AI's team (Noah, Dr. Penkova as PI/advisor, Andy) drops raw meeting notes as messy
bullet fragments — half-finished sentences, character-by-character edit artifacts from live
collaborative typing, nested asides. Someone needs to turn that into a themed, actionable record
before it's useful to anyone else. That's this skill.

## Process

1. **Read the raw notes in full.** Don't skim — collaborative live-editing tools often leave
   fragmented text runs (e.g. "tr" + "ain" + "ing") that only make sense once reassembled.
2. **Group into themes**, not chronological order. Themes that have recurred so far (expect new
   ones as the project evolves — don't force everything into these if a note doesn't fit):
   - Cancer segmentation R&D (model design, the 4-expert ensemble approach, interpretability)
   - Research direction / strategic angle (which condition to lead with, and why)
   - Confidentiality / IP considerations
   - Team logistics (meeting cadence, outreach process, documentation)
   - Funding & operations (donations, events, branding)
3. **Rewrite each raw point as: a clean statement of the point, then a concrete "Next step."**
   A next step should be something a specific person could act on this week, not a restatement of
   the point itself. If the notes already contain enough detail to name who should do it, say so.
4. **Preserve links and direct quotes exactly.** If notes attribute a specific claim or constraint
   to a specific person (e.g. "Dr. Penkova: ..."), keep that attribution — it usually signals a
   standing rule, not just an opinion in passing.
5. **Don't add technical specificity that wasn't in the source notes.** If a raw note gestures at a
   proprietary method without spelling it out, summarize it at the same level of abstraction the
   notes used — don't fill in plausible-sounding technical detail yourself. See "Standing rules"
   below for why this matters here specifically.

## Standing rules to enforce (update this list as new ones come up)

- **Confidentiality:** per Dr. Penkova, cancer-detection methodology (the specific DL/CV
  implementation) should be described publicly only at a high level — never write out a more
  specific version of "how it works" than what's already in the raw notes, even if you could
  infer or generate one. This applies to the tracker doc, any paper draft, and grant narratives.
- **Outreach process:** any email to an external company or organization must be drafted first,
  posted to Discord for Dr. Penkova's QC/sign-off, and only then sent — with her CC'd. Never draft
  a next step that implies sending outreach directly.
- **Team:** meetings should include all three members (Noah, Dr. Penkova, Andy) unless the notes
  say otherwise.

## Output destination

Look for the team's living tracker doc (a Claude Docs artifact, typically titled something like
"BioTransport AI — Funding & Data Tracker," with a main tracker tab and a "Research Notes &
Sources" tab). If you have access to it:

- Add the themed write-up as a dated section (or replace a prior raw-notes dump anchored to the
  same comment thread, if that's what triggered this).
- Pull the highest-priority new next steps into the tracker's "Next steps" checklist.
- Add one dated line to the "Changelog" section summarizing what was reorganized.

If no tracker doc is found or accessible, ask the user where this should go rather than guessing —
don't create a new, competing doc.

## Worked example (structure, not content)

Raw: *"share Andy some ways to get free compute -> put the links and how to in the discord chat.
model training is long and expensive."*

Reorganized: *"Training on a personal PC isn't viable — Andy needs free/low-cost compute. Next
step: post free-compute options (research cloud credits, Colab/Kaggle GPUs, etc.) with links and
how-to in Discord."*

Same information, same links — just legible and pointed at an action.
