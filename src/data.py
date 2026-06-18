"""Загрузка сплитов и применение маппинга code -> group."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass

from src.mapping import map_code

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

SPLIT_FILES = {
    "train": "train_v1.jsonl",
    "dev": "dev_v1.jsonl",
    "test": "test_v1.jsonl",
}


@dataclass
class Dataset:
    texts: list[str]
    codes: list[str]
    labels: list[str]

    def __len__(self) -> int:
        return len(self.texts)


def load_split(split: str, data_dir: str = DATA_DIR) -> Dataset:
    if split not in SPLIT_FILES:
        raise ValueError(f"Неизвестный сплит: {split!r}")
    path = os.path.join(data_dir, SPLIT_FILES[split])
    texts, codes, labels = [], [], []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            texts.append(row["symptoms"])
            codes.append(row["code"])
            labels.append(map_code(row["code"]))
    return Dataset(texts=texts, codes=codes, labels=labels)


def load_all(data_dir: str = DATA_DIR) -> dict[str, Dataset]:
    return {split: load_split(split, data_dir) for split in SPLIT_FILES}
