import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def sales():
    fig, ax = plt.subplots()
    months = ["Січ", "Лют", "Бер", "Кві", "Тра", "Чер"]
    ax.plot(months, [38, 42, 45, 50, 54, 58], "o-", label="План")
    ax.plot(months, [35, 44, 43, 53, 52, 63], "s--", label="Факт")
    ax.set(title="Планові та фактичні продажі", xlabel="Місяць", ylabel="Продажі, тис. грн")
    ax.legend()
    return fig


def ages(rng):
    fig, ax = plt.subplots()
    ages_sample = rng.integers(18, 71, size=100)
    ax.hist(ages_sample, bins=np.arange(15, 76, 5), edgecolor="white")
    ax.axvline(ages_sample.mean(), color="darkorange", linestyle="--",
               label=f"Середній вік: {ages_sample.mean():.1f}")
    ax.set(title="Розподіл віку 100 осіб", xlabel="Вік, років", ylabel="Кількість осіб")
    ax.legend()
    return fig


def exam():
    fig, ax = plt.subplots()
    groups = [[61, 65, 68, 71, 73, 80, 88], [67, 72, 77, 80, 82, 88, 90],
              [54, 60, 72, 78, 87, 93, 99]]
    ax.boxplot(groups)
    ax.set_xticks([1, 2, 3], ["Група A", "Група B", "Група C"])
    ax.set(title="Розкид результатів іспиту", xlabel="Група", ylabel="Бал")
    return fig


def weather():
    fig, ax = plt.subplots()
    humidity_axis = ax.twinx()
    dates = [f"{day:02d}.10" for day in range(5, 12)]
    temperature, = ax.plot(dates, [16, 17, 15, 13, 14, 16, 18], "o-", label="Температура")
    humidity, = humidity_axis.plot(dates, [65, 60, 70, 77, 72, 64, 56], "s--",
                                   color="teal", label="Вологість")
    ax.set(title="Температура та вологість за тиждень", xlabel="Дата", ylabel="Температура, °C")
    humidity_axis.set_ylabel("Відносна вологість, %")
    ax.tick_params(axis="x", labelrotation=35)
    ax.legend(handles=[temperature, humidity], loc="upper left")
    return fig


def server():
    fig, ax = plt.subplots()
    hours = range(24)
    load = [22, 18, 16, 14, 16, 20, 26, 34, 45, 60, 74, 82,
            70, 65, 78, 84, 89, 81, 64, 51, 42, 38, 31, 26]
    ax.plot(hours, load)
    ax.fill_between(hours, load, alpha=0.23)
    ax.set(title="Добове навантаження сервера", xlabel="Година доби",
           ylabel="Навантаження, %", ylim=(0, 100))
    ax.grid(alpha=0.3)
    return fig


def product():
    fig, axes = plt.subplots(2, 2, figsize=(9, 6), sharex=True)
    weeks = [1, 2, 3, 4, 5, 6]
    metrics = [
        ("Конверсія, %", [3.1, 3.2, 2.9, 3.6, 3.8, 4.0]),
        ("Утримання, %", [43, 45, 44, 48, 50, 54]),
        ("Середній чек, грн", [410, 430, 422, 451, 460, 470]),
        ("Замовлення, шт.", [120, 129, 118, 147, 155, 169]),
    ]
    for ax, (label, values) in zip(axes.flat, metrics):
        ax.plot(weeks, values, "o-")
        ax.set_title(label)
        ax.grid(alpha=0.2)
    for ax in axes[1]:
        ax.set_xlabel("Тиждень")
    fig.suptitle("Динаміка метрик продукту")
    return fig


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-show", action="store_true", help="Зберегти PNG без відкриття вікон")
    args = parser.parse_args()
    figures = [sales(), ages(np.random.default_rng(42)), exam(), weather(), server(), product()]
    output = Path(__file__).resolve().parent / "plots"
    output.mkdir(exist_ok=True)
    for number, fig in enumerate(figures, start=1):
        fig.tight_layout()
        fig.savefig(output / f"task_{number}.png", dpi=150)
    if not args.no_show:
        plt.show()


if __name__ == "__main__":
    main()
