# EyePACS (Diabetic Retinopathy Detection)

**Condition:** Diabetes · **Modality:** Fundus images
**Source:** [Kaggle competition](https://www.kaggle.com/c/diabetic-retinopathy-detection) ·
mirrors also exist on [Hugging Face](https://huggingface.co/datasets/ctmedtech/EYEPACS) if the
Kaggle download is unavailable
**Size:** ~35,126 labeled training images (severity grades 0–4, ICDR scale); tens of GB — the
largest of the diabetes datasets here, budget disk space and time accordingly.

## Fetch

```bash
../scripts/fetch_kaggle.sh competition diabetic-retinopathy-detection eyepacs-diabetes
```

You must accept the competition rules on its Kaggle page in a browser first, or the download will
be rejected even with a valid API token. Lands in `data/eyepacs-diabetes/`.
