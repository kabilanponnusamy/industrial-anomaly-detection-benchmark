# Technical review and publication changes

This review is based on the uploaded main notebook and accompanying files. Static checks are not proof of successful end-to-end re-execution. The full MVTec dataset (approximately 5 GB) and trained checkpoints were not supplied, so training, accuracy and latency could not be reproduced independently.

## Original supplied project

- Notebook consists of eight model implementations and a universal training/evaluation/plotting pipeline.
- Loads all available MVTec categories into a joint set, with normal images for model training and both normal/defective images for testing.
- Outputs image scores, pixel heatmaps, embeddings and sometimes reconstruction images. Writes CSV tables and `.pth` checkpoints.
- Other uploaded notebook was an external [Kaggle Anomalib tutorial](https://www.kaggle.com/code/ipythonx/mvtec-ad-anomaly-detection-with-anomalib-library) by Innat, not the core eight-model benchmark; it is linked, not copied, to avoid attribution confusion and large output/image data.

## Issues observed in the original notebook

1. **Test-label leakage:** the decision threshold was selected using a Youden-J statistic computed from the labels of the very test images subsequently evaluated, inflating classification metrics.
2. **Incorrect segmentation threshold:** the image-level threshold was reused to binarize pixel anomaly maps even though their scoring distributions differ.
3. **Dropped test samples:** two initial batches were used only as warmups and entirely skipped from metric calculation (up to 64 test images at batch size 32).
4. **Batch-dependent Hybrid normalization:** global min/max across test batches changed the anomaly map for an image depending on other images present.
5. **Historical reporting inconsistency:** a manually typed results table reported the Hybrid pixel AUROC at 0.7911 and AUPRO 0.5049, while a separate later evaluation output reported 0.7850 and 0.3597. There were duplicated and stale intermediate outputs in the original notebook. Results cannot be treated as a verified single execution history.
6. **Non-standard approximations:** names like DRAEM, GANomaly, FastFlow, CFLOW and PatchCore represent simplified implementations, not faithful research reproductions. CutPaste's pixel map repeats one number over the entire image and cannot localize defects.
7. **Approximate AUPRO:** the implementation subsamples defective images, omits normal test images from false-positive-rate estimation, uses 50 thresholds and a coarse numerical integral. It is **not the official MVTec AUPRO protocol**.
8. **Experimental confounding:** all 15 classes are pooled for training and image-score evaluations. Dataset imbalance and category-specific baselines can make aggregate AUROC misleading; use consistent, category-wise evaluation for proper method comparisons.
9. **Missing portable setup:** original notebook used hardcoded `/content/...` paths, inline shell installers, and an external large dataset. Multiple execution outputs came from a CPU report but other metadata indicated a GPU runtime.
10. **Incomplete reproducibility:** no environment lockfile or runnable model artifacts were attached. Published speed figures cannot be assumed to apply to another machine.

## Corrections in sanitized public notebook

- Removed cell outputs, execution counts and environment metadata to avoid leaking identifiers or presenting stale results.
- Linked external Anomalib tutorial instead of redistributing its notebook; excluded the dataset and all proprietary/unnecessary artifacts.
- Removed inline dataset download commands and hardcoded absolute paths; use `MVTEC_ROOT` and `RESULTS_DIR`.
- Switched pretrained ResNet-18 initialization to the weights-based torchvision API.
- Added **normal-only percentile calibration** for separate image and pixel cutoffs. This avoids direct peeking at test labels, but is still not the independent normal validation split a rigorous benchmark should use.
- Warmup calls no longer exclude test samples.
- Hybrid heatmaps now normalize within each image to avoid cross-image batch dependence. **Per-image normalization can still hurt anomaly classification**, so validate carefully.
- Removed hand-typed metrics table; charts use the current run's exported results.
- Safer checkpoint loading uses `weights_only=True` where supported.

## Remaining research work before production or defensible publication

- Separate normal-only training and validation partitions; calibrate cutoffs on validation, not training and not test.
- Implement canonical versions of methods or explicitly keep them labeled "inspired".
- Fix/replace the approximate AUPRO with official MVTec metric, include nondefective images in false-positive rate.
- Improve Hybrid score fusion with reference-data scaling, not per-image minmax.
- Establish category-specific training/evaluation; repeated random seeds; confidence intervals; measured hardware and software versions.
- Require ground-truth masks and reliable annotation protocols for real defects. Confirm generalization to unseen factory image/camera conditions.
- Package and test a reproducible inference API before any deployment; add sensitivity/specificity analysis and human-in-the-loop failure handling.

## Security/privacy review

Main notebook source showed no obvious credential assignments, token strings, or personally identifying author text. Original source filenames contained a numeric academic identifier and were changed. Raw cell outputs, the original ZIP, the research submission DOCX and the external Anomalib tutorial are not included. The optional PowerShell helper uses a GitHub no-reply email address for Git commit metadata, instead of the machine’s configured college or personal email. This is a practical static review, not a formal security certification.
