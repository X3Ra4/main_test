import csv
from pathlib import Path

import numpy as np


NUMERIC = ("lotsize", "bedrooms", "bathrms")
CATEGORICAL = ("driveway", "airco")


def encode(row):
    return [float(row[key]) for key in NUMERIC] + [
        float({"yes": 1, "no": 0}[row[key].strip().lower()]) for key in CATEGORICAL
    ]


def gradient_descent(features, target, learning_rate=0.05, iterations=2000):
    weights = np.zeros(features.shape[1])
    loss_history = []
    for step in range(iterations):
        errors = features @ weights - target
        if step % 100 == 0:
            loss_history.append(float(np.mean(errors ** 2)))
        gradient = 2 * (features.T @ errors) / len(target)
        weights -= learning_rate * gradient
    loss_history.append(float(np.mean((features @ weights - target) ** 2)))
    return weights, loss_history


def main():
    with Path(__file__).with_name("Housing.csv").open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    features = np.asarray([encode(row) for row in rows])
    target = np.asarray([float(row["price"]) for row in rows])
    permutation = np.random.default_rng(42).permutation(len(rows))
    test_size = int(np.ceil(len(rows) * 0.2))
    test, train = permutation[:test_size], permutation[test_size:]
    mean, scale = features[train].mean(axis=0), features[train].std(axis=0)
    scale = np.where(scale == 0, 1, scale)

    def design(values):
        return np.column_stack((np.ones(len(values)), (values - mean) / scale))

    weights, losses = gradient_descent(design(features[train]), target[train])
    predictions = design(features[test]) @ weights
    errors = target[test] - predictions
    r2 = 1 - np.sum(errors ** 2) / np.sum((target[test] - target[test].mean()) ** 2)
    house = dict(lotsize=5000, bedrooms=3, bathrms=2, driveway="yes", airco="no")
    predicted_price = (design(np.asarray([encode(house)])) @ weights)[0]

    print(f"Спостережень: {len(rows)}. Train: {len(train)}. Test: {len(test)}.")
    print(f"MSE навчання: {losses[0]:,.0f} → {losses[-1]:,.0f}")
    print(f"Тест: MAE = {np.abs(errors).mean():,.2f}, R² = {r2:.4f}")
    print("Характеристики будинку:", house)
    print(f"Прогноз ціни у валюті датасету: {predicted_price:,.2f}")
    assert np.isfinite(predicted_price) and losses[-1] < losses[0]


if __name__ == "__main__":
    main()
