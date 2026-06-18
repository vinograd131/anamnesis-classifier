"""Маппинг кодов МКБ-10 в группы фитнес-ограничений."""

from __future__ import annotations

# Спорные коды (нужна мед. проверка): G54 -> spine (радикулопатия), G43/G44 ->
# neuro_balance, D50 -> none (можно metabolic), J30/J35 -> none.
GROUPS: dict[str, list[str]] = {
    "spine": ["M54", "M53", "M51", "M42", "G54"],
    "joints": ["M13", "M19", "M02", "M17", "M75", "M77", "M05", "M15", "M10", "M06"],
    "cardio": ["I11", "I67", "I10", "I20", "I49", "I83", "I25"],
    "metabolic": ["E06", "E66", "E04", "E11", "E01", "E05", "E89", "E28",
                  "E03", "E22", "E74", "E27"],
    "respiratory": ["J45", "J44", "J42", "J41", "J84"],
    "neuro_balance": ["G90", "G44", "G20", "G40", "G52", "G98", "G43", "G25",
                      "G62", "G56", "G30", "G37", "G35", "G50", "G96", "H81"],
    "core_visceral": ["N41", "N76", "N30", "N20", "N95", "N80", "N97", "N83",
                      "N86", "N40", "N81", "N39", "N28", "N93", "N84", "N91",
                      "N94", "N34", "N92", "K29", "K21", "K81", "K80", "K58",
                      "K26", "K52", "K64", "D25"],
    "acute": ["J06", "J00", "J01", "J02", "J18", "J20"],
    "none": ["L30", "L40", "L20", "L21", "L70", "L71", "L50", "J30", "J31",
             "J32", "J35", "D50", "D23", "H65", "F41", "Z00"],
}

CLASS_NAMES: list[str] = list(GROUPS.keys())

CODE_TO_GROUP: dict[str, str] = {
    code: group for group, codes in GROUPS.items() for code in codes
}

DEFAULT_GROUP = "none"


def map_code(code: str, *, strict: bool = False) -> str:
    key = code.strip().upper()
    if key in CODE_TO_GROUP:
        return CODE_TO_GROUP[key]
    if strict:
        raise KeyError(f"Код вне маппинга: {code!r}")
    return DEFAULT_GROUP


def uncovered_codes(codes) -> set[str]:
    return {c.strip().upper() for c in codes if c.strip().upper() not in CODE_TO_GROUP}
