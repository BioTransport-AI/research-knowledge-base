# IDRiD (Indian Diabetic Retinopathy Image Dataset)

**Condition:** Diabetes · **Modality:** Fundus images with pixel-level lesion annotations
**Source:** [IEEE DataPort](https://ieee-dataport.org/open-access/indian-diabetic-retinopathy-image-dataset-idrid)
**License:** CC BY 4.0 (stated as open access on the source page)
**Size:** 516 images — the smallest of the diabetes imaging sets here.

## No fetch script — verify the download mechanism first

IEEE DataPort doesn't expose a stable, unauthenticated download URL I could confirm without an
account, and I'm not going to script against a guessed one. Visit the link above, check what
access it actually requires today (may just need a free account), and download manually into
`data/idrid-diabetes/`. If it turns out to be a simple stable URL once you're in, a `fetch.sh`
here would be easy to add — just don't want to ship one I haven't verified works.
