import json
import platform
from pathlib import Path
from time import perf_counter

import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_auc_score, accuracy_score, f1_score, precision_score, recall_score,
)


def main():
    folder = Path(__file__).resolve().parent
    print("Loading dataset...", flush=True)
    start = perf_counter()
    data = pd.read_csv(folder / "creditcard.csv")
    load_time = perf_counter() - start
    X, y = data.drop(columns=["Class"]), data["Class"]
    X_dev, X_test, y_dev, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_dev, y_dev, test_size=0.2, stratify=y_dev, random_state=42
    )
    model = lgb.LGBMClassifier(
        objective="binary", n_estimators=1000, learning_rate=0.05,
        num_leaves=31, n_jobs=2, random_state=42, verbosity=-1,
    )
    print("Training LightGBM...", flush=True)
    start = perf_counter()
    model.fit(
        X_train, y_train, eval_set=[(X_val, y_val)], eval_metric="auc",
        callbacks=[lgb.early_stopping(50, verbose=False)],
    )
    training_time = perf_counter() - start
    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)

    one_row = X_test.iloc[:1].copy()
    batch = X_test.iloc[:1000].copy()
    model.predict_proba(one_row)
    model.predict_proba(batch)
    single_repeats, batch_repeats = 100, 20
    start = perf_counter()
    for _ in range(single_repeats):
        model.predict_proba(one_row)
    latency_ms = (perf_counter() - start) / single_repeats * 1000
    start = perf_counter()
    for _ in range(batch_repeats):
        model.predict_proba(batch)
    throughput = len(batch) * batch_repeats / (perf_counter() - start)

    result = {
        "load_data_time_seconds": load_time,
        "training_time_seconds": training_time,
        "best_iteration": int(model.best_iteration_),
        "auc_roc": float(roc_auc_score(y_test, probabilities)),
        "accuracy": float(accuracy_score(y_test, predictions)),
        "f1_score": float(f1_score(y_test, predictions, zero_division=0)),
        "precision": float(precision_score(y_test, predictions, zero_division=0)),
        "recall": float(recall_score(y_test, predictions, zero_division=0)),
        "inference_latency_1_row_ms": latency_ms,
        "inference_throughput_rows_per_second": throughput,
        "benchmark_config": {
            "seed": 42, "prediction_threshold": 0.5,
            "train_rows": len(X_train), "validation_rows": len(X_val),
            "test_rows": len(X_test), "test_fraud_rows": int(y_test.sum()),
            "threads": 2, "latency_repeats": single_repeats,
            "throughput_batch_rows": len(batch),
            "throughput_repeats": batch_repeats,
            "lightgbm_version": lgb.__version__,
            "python_version": platform.python_version(),
        },
    }
    output = folder / "benchmark_result.json"
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("\n| Metric | Result |\n|---|---|")
    for name, value in result.items():
        if name != "benchmark_config":
            formatted = str(value) if isinstance(value, int) else f"{value:.6f}"
            print(f"| {name} | {formatted} |")
    print(f"\nSaved: {output}")


if __name__ == "__main__":
    main()
