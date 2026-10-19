"""Offline unit tests for dataset path validation; no actual MVTec images are used."""
import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_dataset.py"
spec = importlib.util.spec_from_file_location("check_dataset", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_missing_dataset_root(tmp_path):
    assert mod.verify(tmp_path / "absent")


def test_complete_synthetic_folder_structure(tmp_path):
    for cat in mod.EXPECTED:
        for folder in ("train/good", "test/good", "ground_truth"):
            (tmp_path / cat / folder).mkdir(parents=True, exist_ok=True)
    assert mod.verify(tmp_path) == []


def test_missing_category_detected(tmp_path):
    (tmp_path / "bottle" / "train" / "good").mkdir(parents=True)
    assert any("Missing category" in issue for issue in mod.verify(tmp_path))
