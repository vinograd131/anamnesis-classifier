"""Метрики и отчёты (основная — macro-F1)."""

from __future__ import annotations

import os

from sklearn.metrics import classification_report, confusion_matrix, f1_score

from src.mapping import CLASS_NAMES


def macro_f1(y_true, y_pred) -> float:
    return f1_score(y_true, y_pred, labels=CLASS_NAMES, average="macro", zero_division=0)


def report_text(y_true, y_pred) -> str:
    return classification_report(
        y_true, y_pred, labels=CLASS_NAMES, zero_division=0, digits=3
    )


def confusion_text(y_true, y_pred) -> str:
    cm = confusion_matrix(y_true, y_pred, labels=CLASS_NAMES)
    short = [c[:6] for c in CLASS_NAMES]
    header = "true\\pred".ljust(14) + "".join(s.rjust(8) for s in short)
    lines = [header]
    for name, row in zip(short, cm, strict=True):
        lines.append(name.ljust(14) + "".join(str(v).rjust(8) for v in row))
    return "\n".join(lines)


def save_confusion_matrix(y_true, y_pred, path: str, title: str = "Confusion matrix"):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from sklearn.metrics import ConfusionMatrixDisplay

    cm = confusion_matrix(y_true, y_pred, labels=CLASS_NAMES)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=CLASS_NAMES)
    fig, ax = plt.subplots(figsize=(9, 8))
    disp.plot(ax=ax, xticks_rotation=45, cmap="Blues", colorbar=False)
    ax.set_title(title)
    fig.tight_layout()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path
