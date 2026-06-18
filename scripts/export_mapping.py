"""Сгенерировать data/label_mapping.json и показать распределение групп."""

from __future__ import annotations

import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding="utf-8")

from src.data import load_all  # noqa: E402
from src.mapping import CLASS_NAMES, CODE_TO_GROUP, GROUPS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def export_json() -> str:
    out = os.path.join(ROOT, "data", "label_mapping.json")
    payload = {
        "version": 1,
        "class_names": CLASS_NAMES,
        "groups": GROUPS,
        "code_to_group": CODE_TO_GROUP,
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return out


def show_distribution() -> None:
    splits = load_all()
    counters = {s: collections.Counter(ds.labels) for s, ds in splits.items()}
    print(f"{'group':16} {'train':>7} {'dev':>6} {'test':>6}")
    print("-" * 38)
    for group in CLASS_NAMES:
        print(f"{group:16} {counters['train'][group]:7} "
              f"{counters['dev'][group]:6} {counters['test'][group]:6}")
    print("-" * 38)
    print(f"{'ИТОГО':16} {len(splits['train']):7} "
          f"{len(splits['dev']):6} {len(splits['test']):6}")


if __name__ == "__main__":
    print(f"Записан {export_json()}\n")
    show_distribution()
