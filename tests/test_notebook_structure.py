"""Lightweight tests that do not need the MVTec dataset or model training."""
import json
from pathlib import Path

NOTEBOOK = Path(__file__).resolve().parents[1] / "notebooks" / "anomaly_detection_benchmark.ipynb"

def test_valid_notebook_and_no_outputs():
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    assert nb["nbformat"] == 4
    assert all(cell.get("outputs", []) == [] and cell.get("execution_count") is None
               for cell in nb["cells"] if cell["cell_type"] == "code")

def test_model_definitions_and_calibration():
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    content = "\n".join("".join(c["source"]) for c in nb["cells"])
    for name in ("ConvAutoencoder", "GANAnomaly", "DRAEM", "CutPasteDetector",
                 "PatchCore", "FastFlow", "CFLOW", "HybridAnomalyModel"):
        assert "class " + name in content
    assert "def calibrate_thresholds" in content
    assert "image_threshold=image_threshold" in content
    assert "pixel_threshold=pixel_threshold" in content
    assert "compute_optimal_threshold(gt_labels" not in content

def test_python_cell_syntax():
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] == "code":
            compile("".join(cell["source"]), f"cell_{i}", "exec")
