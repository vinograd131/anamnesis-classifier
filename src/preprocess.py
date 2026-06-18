"""Нормализация текста жалоб."""

from __future__ import annotations

import re

_WHITESPACE_RE = re.compile(r"\s+")
_ALLOWED_RE = re.compile(r"[^0-9a-zA-Zа-яёА-ЯЁ\s.,;:%()/-]+")


def normalize(text: str) -> str:
    # Отрицания не трогаем: "нет"/"без"/"не" меняют класс.
    text = text.lower().replace("ё", "е")
    text = _ALLOWED_RE.sub(" ", text)
    text = _WHITESPACE_RE.sub(" ", text)
    return text.strip()


def normalize_all(texts) -> list[str]:
    return [normalize(t) for t in texts]
