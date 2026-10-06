---
name: biotransport-outreach-email
description: Draft outreach emails to prospective funders and data providers for BioTransport AI (diabetes, anemia, glaucoma, cancer-imaging research). Use this whenever Noah, Dr. Penkova, or Andy asks to reach out to a funder/foundation/agency or a dataset owner, wants to "draft an email to" a specific organization, or asks to turn tracker rows into outreach, even if they don't name this skill directly. Always produces drafts for review, never sends anything.
---

# BioTransport AI outreach email drafting

BioTransport AI's funding and data leads live as rows in the team's tracker doc. Turning a row
into an actual email that's worth a stranger's time, and that Dr. Penkova will actually approve,
takes real research per organization, not a template with the name swapped in. That's this skill.

## Process

1. **Pull the current candidate list from the tracker's "Funding tracker" and "Data sources
   tracker" tables**, not from memory. Re-read the live doc first, since rows and statuses change
   between sessions.
2. **Filter before drafting.** Don't draft an email for every row reflexively:
   - Skip anything marked "Not now" or with a closed application cycle unless a *lighter*,
     early-relationship email genuinely makes sense (e.g., introducing the team ahead of next
     year's window). If so, say explicitly that it's not an application, just an introduction.
   - Skip programs that structurally don't take unsolicited outreach (e.g., ARPA-H doesn't
     publish Program Manager emails and works through solicitation cycles). For those, draft
     something scoped to what their actual process allows (a fit question through their listed
     channel), not a pitch that ignores how they operate.
   - A mismatched program (e.g., a fund scoped to a population or condition BioTransport doesn't
     serve) doesn't get an email. Note why it's excluded instead.
3. **Research each remaining organization before drafting anything**, specifically:
   - A verifiable contact (named person plus email, or the documented request channel, portal, or
     form). **Never invent a plausible-looking email address.** If you can't verify one, say so
     plainly in the draft and name where to look (e.g., "check the paper's corresponding author,"
     "use the site's contact form"). A flagged gap is useful; a guessed address wastes everyone's
     time and looks unprofessional if it bounces or reaches the wrong person.
   - Their mission and priorities, so the email can speak to what *they* care about, not just what
     BioTransport wants.
   - A concrete "why us," grounded in what BioTransport has actually built or found (a live
     product, a specific precedent project they've funded before, a real methodological angle),
     never generic enthusiasm.
   - A concrete "what's in it for them": for funders, fit with their stated priorities and a
     fundable or novel angle; for data providers, proper citation, compliance with their usage
     terms, and where real, a contribution back (sharing validated tooling, results, or
     co-authorship).
4. **Draft each email** with: Subject line, Send-to (with verification status), and a body under
   ~250 words covering intent, the specific ask, why-us, and what's-in-it-for-them. Keep it
   scannable. These are being read by busy program officers and lab managers, not colleagues.
   - **If the user has already sent or restyled one of these emails themselves** (pasted a
     screenshot or final version), treat that as the house style going forward: match its
     greeting convention, tone, formatting (bold, links), and closing for the rest of the batch,
     not the earlier generic draft. Their actual sent copy always wins over a first-pass template.
   - **Only claim a product is "already live" when it actually is.** Diabetes and anemia screening
     are live; glaucoma imaging is not (the live glaucoma product is a chatbot, not a screener).
     For glaucoma-imaging asks, frame it honestly as extending the team's existing, proven
     approach rather than implying the glaucoma tool already exists.
   - **If the user says they'll add their own signature, stop at the closing line** (e.g., "Thank
     you for your time.") and don't draft a name/title/contact block. That avoids drafting
     something that gets silently overwritten or duplicated.
5. **Note who should send it.** Funder and program-officer contacts (especially NIH-style
   pre-submission inquiries) are normally most credible coming from the PI (Dr. Penkova) directly.
   Data-access requests can reasonably come from any team member. Say which, don't just default to
   one signature.
6. **When a reply comes in, close the loop in the tracker before moving on.** Add a "Reply
   received" note under the original draft with what was actually said, correct anything in the
   Funding/Data tables that the reply contradicts (learned the hard way: a "free GCP credits" perk
   the team had researched turned out to be stale info IDC itself hadn't updated, so verify a
   claimed perk or deadline is still true rather than trusting a research pass from days earlier),
   and draft any necessary follow-up as a new dated sub-item rather than editing the original send
   record.
7. **A data-hosting support desk isn't the same as a grant program's officers**, even when one
   organization runs both (e.g., NCI IDC support is not NCI ITCR program administration). If an
   inquiry about funding fit and a request about data access both plausibly go to the same general
   inbox, send them as separate emails to the most specific contact for each, not one email to
   whichever address is easiest to find.

## Standing rules to enforce

- **No USC, anywhere, full stop** (updated 2026-09-22, Dr. Penkova, in Discord: "remove USC from
  every line. If we integrate one day and it works for us, then we can include the USC name.").
  Not the signature, not the body, not "USC-affiliated," not "Our team at USC." Every reference is
  just "BioTransport AI." This applies even to the NIH pre-submission email, which is signed by
  Dr. Penkova as PI. Her USC appointment is real, but the rule is now blanket until she says
  otherwise, not a case-by-case judgment call.
- **Confidentiality:** describe cancer-detection methodology only at the level of abstraction
  already used elsewhere (e.g., "an ensemble-based approach," "advanced computational methods").
  Never spell out the specific implementation, even to make an email sound more impressive.
- **Outreach QC:** every draft goes to Dr. Penkova (and Andy) for review before anything sends.
  This skill drafts, it never sends and never implies the draft is final. Say so explicitly if
  producing a batch of drafts, so nobody mistakes "drafted" for "sent."
- **Team:** BioTransport AI, PI Dr. Penkova. See the root `CLAUDE.md` for the USC rule above; do
  not describe the team as "USC-affiliated" in any draft.

## Output destination

Add drafts to the tracker doc's "Outreach Drafts" tab (create it if it doesn't exist yet, following
the same tab pattern as "Research Notes & Sources"), organized under **Funding** and **Data**
headings, numbered, each with Send-to / Subject / the draft body as a blockquote. Add one dated
Changelog line summarizing what was drafted and flagging any unverified contacts. Don't just paste
drafts into chat and call it done. The tracker doc is where Dr. Penkova and Andy actually review
things.
