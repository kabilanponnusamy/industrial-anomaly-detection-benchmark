# Dataset — MVTec AD

This folder documents how to obtain the **MVTec AD** industrial visual anomaly-detection benchmark. **No dataset images or masks are published in this repository.**

## Download and attribution

- **Official source:** https://www.mvtec.com/research-teaching/datasets/mvtec-ad
- **Kaggle mirror referenced by the supplied research artifact:** https://www.kaggle.com/datasets/ipythonx/mvtec-ad
- **Original research:** Bergmann, P., Fauser, M., Sattlegger, D., Steger, C. (2019), *MVTec AD — A Comprehensive Real-World Dataset for Unsupervised Anomaly Detection*, CVPR.
- **Terms:** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) for the MVTec images. Commercial use is not permitted under this license without permission. See the official page for the definitive terms.

The dataset contains more than 5,000 images across **15 object and texture categories**, organized into normal training images, normal/defective test images, and pixel-accurate masks for known defects.

## Local layout

Download the dataset yourself, then extract the folders *inside* `datasets/mvtec_ad/`:

```text
datasets/
├── README.md
└── mvtec_ad/                  ← ignored; not included on GitHub
    ├── bottle/
    │   ├── train/good/
    │   ├── test/good/
    │   ├── test/broken_large/
    │   └── ground_truth/broken_large/
    ├── cable/
    ├── capsule/
    └── ...
```

**Validate after extraction:**

```bash
python scripts/check_dataset.py datasets/mvtec_ad
```

The notebook's default dataset path is `./datasets/mvtec_ad`, so the layout above works without setting an environment variable. If you store the dataset elsewhere, point the notebook to that directory:

```powershell
# Windows PowerShell
$env:MVTEC_ROOT = 'datasets/mvtec_ad'
```

```bash
# macOS/Linux
export MVTEC_ROOT=datasets/mvtec_ad
```

The environment variable must identify the *parent* of the `bottle/`, `cable/`, etc. folders.

### Why not commit 5 GB of images?

- The dataset has its **own copyright and non-commercial use terms**.
- Binary images are too large and inefficient for normal Git history.
- Visitors should download the authoritative version directly, keeping code review and cloning fast.

**Do not add** `datasets/mvtec_ad/`, dataset archives, mask files, pre-trained checkpoints or credential files to Git.
