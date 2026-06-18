"""Тесты маппинга code -> group."""

from __future__ import annotations

import json
import os

import pytest

from src.mapping import CODE_TO_GROUP, GROUPS, map_code, uncovered_codes

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
SPLITS = ["train_v1.jsonl", "dev_v1.jsonl", "test_v1.jsonl"]


def _load_codes(filename: str) -> list[str]:
    path = os.path.join(DATA_DIR, filename)
    codes = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                codes.append(json.loads(line)["code"])
    return codes


def test_each_code_in_exactly_one_group():
    seen: dict[str, str] = {}
    for group, codes in GROUPS.items():
        for code in codes:
            assert code not in seen, f"{code} в двух группах: {seen.get(code)} и {group}"
            seen[code] = group
    assert len(seen) == len(CODE_TO_GROUP)


@pytest.mark.parametrize("split", SPLITS)
def test_all_dataset_codes_covered(split):
    missing = uncovered_codes(_load_codes(split))
    assert not missing, f"{split}: коды вне маппинга: {sorted(missing)}"


def test_train_class_counts_sum_to_total():
    codes = _load_codes("train_v1.jsonl")
    counts: dict[str, int] = {}
    for code in codes:
        counts[map_code(code)] = counts.get(map_code(code), 0) + 1
    assert sum(counts.values()) == len(codes)
    assert set(counts) == set(GROUPS)


def test_map_code_strict_raises_on_unknown():
    with pytest.raises(KeyError):
        map_code("X99", strict=True)


def test_map_code_default_for_unknown():
    assert map_code("X99") == "none"
