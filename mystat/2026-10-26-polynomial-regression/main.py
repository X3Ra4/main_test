import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures


def split(features, target):
    return train_test_split(features, target, test_size=0.2, random_state=42)


def main():
    data = fetch_california_housing()
    train, test, y_train, y_test = split(data.data[:, [0]], data.target)
    polynomial_scores = []
    for degree in (1, 2, 3):
        model = make_pipeline(PolynomialFeatures(degree=degree, include_bias=False), LinearRegression())
        model.fit(train, y_train)
        polynomial_scores.append((degree, model.score(train, y_train), model.score(test, y_test)))

    print(f"Завдання 1. Поліном ступеня 2: тестове R² = {polynomial_scores[1][2]:.4f}")
    print("\nЗавдання 2. Порівняння ступенів")
    print("| Ступінь | R² train | R² test |\n|---:|---:|---:|")
    for degree, train_score, test_score in polynomial_scores:
        print(f"| {degree} | {train_score:.4f} | {test_score:.4f} |")

    names = ["MedInc", "HouseAge", "AveRooms", "AveBedrms"]
    columns = [data.feature_names.index(name) for name in names]
    train, test, y_train, y_test = split(data.data[:, columns], data.target)
    linear = LinearRegression().fit(train, y_train)
    lasso = Lasso(alpha=0.1).fit(train, y_train)
    ridge = Ridge(alpha=1.0).fit(train, y_train)

    print("\nЗавдання 3. LinearRegression і Lasso")
    print(f"Тестове R²: LinearRegression = {linear.score(test, y_test):.4f}; "
          f"Lasso = {lasso.score(test, y_test):.4f}")
    print("| Ознака | LinearRegression | Lasso |\n|---|---:|---:|")
    for name, linear_coef, lasso_coef in zip(names, linear.coef_, lasso.coef_):
        print(f"| {name} | {linear_coef:.5f} | {lasso_coef:.5f} |")
    print(f"Нульових коефіцієнтів у Lasso: {np.count_nonzero(lasso.coef_ == 0)}")

    print("\nЗавдання 4. LinearRegression і Ridge")
    print("| Модель | R² test | Ненульових коефіцієнтів |\n|---|---:|---:|")
    for name, model in (("LinearRegression", linear), ("Ridge (alpha=1.0)", ridge)):
        print(f"| {name} | {model.score(test, y_test):.4f} | {np.count_nonzero(model.coef_)} |")


if __name__ == "__main__":
    main()
