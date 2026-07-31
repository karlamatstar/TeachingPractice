from pathlib import Path

import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "_OUTPUT" / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


train_df = pd.read_csv(
    DATA_DIR / "train_data.csv",
    encoding="utf-8-sig"
)


routing_classifier = Pipeline(
    steps=[
        (
            "vectorizer",
            TfidfVectorizer(
                analyzer="char",
                ngram_range=(2, 5)
            )
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                random_state=42
            )
        )
    ]
)


routing_classifier.fit(
    train_df["text"],
    train_df["label"]
)


joblib.dump(
    routing_classifier,
    MODEL_DIR / "routing_classifier.joblib"
)
