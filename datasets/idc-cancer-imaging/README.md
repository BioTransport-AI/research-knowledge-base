# NCI Imaging Data Commons (IDC)

**Condition:** Cancer · **Modality:** Imaging (CT/MRI/etc.), cloud-hosted
**Source:** [IDC AI-Assistants Guide](https://learn.canceridc.dev/ai-assistants/agents) ·
[portal](https://portal.imaging.datacommons.cancer.gov/)

## This one doesn't get bulk-downloaded at all

IDC isn't a fixed set of files to fetch once — it's a large, actively-growing cloud collection
meant to be queried live. Per IDC's own team (Andrey Fedorov, replying to our outreach — see
Outreach Drafts, email 5), their recommended access path is now an **agentic interface** (an MCP
server an AI agent can query directly), not manual browsing or a bulk download.

There's no `fetch.sh` here because there's nothing to fetch in advance — the workflow is: an
agent (or a human, via the portal) queries IDC directly for the specific collection/cohort needed,
at the time it's needed. Set up the agentic interface per the guide linked above when cancer-imaging
work actually starts; nothing to do here until then.
