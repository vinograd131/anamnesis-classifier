"""Обучить TF-IDF baseline на train, оценить на dev, сохранить отчёт."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding="utf-8")

from src.data import load_split  # noqa: E402
from src.metrics import confusion_text, macro_f1, report_text  # noqa: E402
from src.models.tfidf_baseline import train  # noqa: E402
from src.preprocess import normalize_all  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main() -> None:
    train_ds = load_split("train")
    dev_ds = load_split("dev")

    pipe = train(normalize_all(train_ds.texts), train_ds.labels)
    pred = pipe.predict(normalize_all(dev_ds.texts))
    f1 = macro_f1(dev_ds.labels, pred)

    cm = confusion_text(dev_ds.labels, pred)
    print(f"\n=== TF-IDF baseline (dev) ===\nmacro-F1: {f1:.4f}\n")
    print(report_text(dev_ds.labels, pred))
    print("\nConfusion matrix (true \\ pred):\n")
    print(cm)

    report_path = os.path.join(ROOT, "reports", "tfidf_baseline_dev.txt")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"TF-IDF baseline (dev)\nmacro-F1: {f1:.4f}\n\n")
        f.write(report_text(dev_ds.labels, pred))
        f.write("\n\nConfusion matrix (true \\ pred):\n\n")
        f.write(cm)
    print(f"\nОтчёт → {report_path}")


if __name__ == "__main__":
    main()
