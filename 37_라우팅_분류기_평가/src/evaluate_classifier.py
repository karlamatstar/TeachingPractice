from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "_OUTPUT" / "models"
REPORT_DIR = BASE_DIR / "_OUTPUT" / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


test_df = pd.read_csv(
    DATA_DIR / "test_data.csv",
    encoding="utf-8-sig"
)

routing_classifier = joblib.load(
    MODEL_DIR / "routing_classifier.joblib"
)

predictions = routing_classifier.predict(
    test_df["text"]
)

accuracy = accuracy_score(
    test_df["label"],
    predictions
)

report_text = classification_report(
    test_df["label"],
    predictions,
    digits=4
)

labels = [
    "sports_agent",
    "timer_agent",
    "order_agent",
    "general_chat"
]

matrix = confusion_matrix(
    test_df["label"],
    predictions,
    labels=labels
)

display = ConfusionMatrixDisplay(
    confusion_matrix=matrix,
    display_labels=labels
)

display.plot(
    xticks_rotation=30
)

plt.tight_layout()

plt.savefig(
    REPORT_DIR / "confusion_matrix.png",
    dpi=150
)

evaluation_df = test_df.copy()
evaluation_df["predicted_label"] = predictions
evaluation_df["is_correct"] = (
    evaluation_df["label"]
    == evaluation_df["predicted_label"]
)

evaluation_df.to_csv(
    REPORT_DIR / "test_result.csv",
    index=False,
    encoding="utf-8-sig"
)
