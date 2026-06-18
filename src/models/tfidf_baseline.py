"""TF-IDF + логистическая регрессия (CPU)."""

from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion, Pipeline

from src.config import SEED


def build_pipeline() -> Pipeline:
    word_vec = TfidfVectorizer(
        analyzer="word", ngram_range=(1, 2), min_df=2, sublinear_tf=True
    )
    # char-граммы добирают опечатки и морфологию шумного медтекста.
    char_vec = TfidfVectorizer(
        analyzer="char_wb", ngram_range=(3, 5), min_df=2, sublinear_tf=True
    )
    features = FeatureUnion([("word", word_vec), ("char", char_vec)])
    clf = LogisticRegression(
        max_iter=2000, class_weight="balanced", C=4.0, random_state=SEED
    )
    return Pipeline([("features", features), ("clf", clf)])


def train(texts, labels) -> Pipeline:
    pipe = build_pipeline()
    pipe.fit(texts, labels)
    return pipe
