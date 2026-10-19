# Historical Results — Context and Caveats

> **Not independently reproduced.** The values below were recorded in the uploaded original notebook's saved execution outputs, before cleanup. They are not results of a fresh training run, and should not be used as an algorithm leaderboard or a production quality claim.

| Simplified / research baseline | Recorded image AUROC | Recorded pixel AUROC |
|---|---:|---:|
| Autoencoder | 0.5417 | 0.6188 |
| GAN | 0.5641 | 0.5430 |
| CutPaste | 0.4581 | 0.5498 |
| PatchCore | 0.5221 | 0.7592 |
| FastFlow | 0.5258 | 0.7602 |
| DRAEM | 0.4637 | 0.5908 |
| CFLOW | 0.4212 | 0.4886 |
| Hybrid (last printed evaluation) | 0.5042 | 0.7850 |

## Interpreting the observation responsibly

Pixel-level AUROC and image-level AUROC answer different questions. In these saved outputs some methods show stronger pixel rankings than image rankings, but **image AUROC values near 0.5 imply poor whole-image anomaly ranking**. These observations are **not evidence of reliable product-level quality control**.

## Why the original results cannot be treated as a definitive benchmark

1. **Test-label leakage:** the prior notebook chose its operating cutoff from test labels; precision, recall and F1 may therefore be optimistic or distorted.
2. **Conflicting runs:** a separately displayed earlier Hybrid result reported **image AUROC 0.5269 and pixel AUROC 0.7911**, whereas the last printed evaluation reported **0.5042 / 0.7850**. A manually typed final comparison reused the earlier numbers. They are from inconsistent contexts and must not be blended.
3. **Simplified model versions:** this repository's implementations must not be compared directly against paper-reported canonical versions.
4. **Evaluation differences:** the original approximate AUPRO, thresholding, mixed-category training, and hardware/runtime environment make cross-study comparison unsafe.
5. **Post-cleanup results pending:** the cleaned notebook removes saved outputs, revises some code and uses current-run CSV exports; no new full-MVTec evaluation has been completed.

## Reproduce a new comparison

Follow the [README](../README.md), download the dataset via [`datasets/README.md`](../datasets/README.md), execute the clean notebook from top to bottom, and use the newly generated `results/Master_Model_Comparison.csv`. For scientific-quality claims, first address the remaining issues in [the technical review](technical-review.md).
