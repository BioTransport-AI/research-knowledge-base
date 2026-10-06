# APTOS 2019 Blindness Detection

**Condition:** Diabetes · **Modality:** Fundus images
**Source:** [Kaggle competition](https://www.kaggle.com/c/aptos2019-blindness-detection)
**Size:** ~3,662 labeled images (severity grades 0–4), a few GB, much smaller than EyePACS.

## Fetch

```bash
../scripts/fetch_kaggle.sh competition aptos2019-blindness-detection aptos2019-diabetes
```

Accept the competition rules on its Kaggle page in a browser first. Lands in
`data/aptos2019-diabetes/`.
