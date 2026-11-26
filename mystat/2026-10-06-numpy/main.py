import numpy as np


def integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введіть ціле число.")


def bounds(message, valid=lambda low, high: low <= high):
    while True:
        low = integer("Нижня межа: ")
        high = integer("Верхня межа: ")
        if valid(low, high):
            return low, high
        print(message)


def shape(matrix_size=None):
    while True:
        rows = integer("Рядки: ")
        columns = integer("Стовпці: ")
        if rows > 0 and columns > 0 and (matrix_size is None or rows * columns == matrix_size):
            return rows, columns
        print("Розміри мають бути додатними й зберігати кількість елементів.")


def main():
    rng = np.random.default_rng(42)
    print("\n1. Пошук і сортування")
    values = rng.integers(0, 50, 20, endpoint=True)
    print("Масив:", values)
    threshold = integer("Поріг: ")
    print("Вище порогу:", np.count_nonzero(values > threshold))
    print("Максимум та його перший індекс (від 0):", values.max(), values.argmax())
    print("За спаданням:", np.sort(values)[::-1])

    print("\n2. Головна діагональ")
    low, high = bounds("Нижня межа не може перевищувати верхню.")
    matrix = rng.integers(low, high, (5, 5), endpoint=True)
    diagonal = matrix.diagonal()
    print(matrix)
    print("Діагональ:", diagonal, "Сума:", diagonal.sum())
    print("З нулями над діагоналлю:\n", np.tril(matrix))

    print("\n3. Рядки та стовпці")
    low, high = bounds("Включний діапазон має містити рівно 30 чисел.", lambda a, b: b - a == 29)
    matrix = np.arange(low, high + 1).reshape(6, 5)
    print(matrix)
    print("Суми рядків:", matrix.sum(axis=1))
    print("Максимуми стовпців:", matrix.max(axis=0))

    print("\n4. Від’ємні значення")
    low, high = bounds("Вкажіть коректний діапазон з від’ємною нижньою межею.", lambda a, b: a < 0 and a <= b)
    values = rng.integers(low, high, 15, endpoint=True)
    print("Масив:", values)
    print("Від’ємні:", values[values < 0])
    changed = np.maximum(values, 0)
    print("Копія:", changed, "Кількість нулів:", np.count_nonzero(changed == 0))

    print("\n5. Операції над масивами")
    length = integer("Довжина: ")
    while length <= 0:
        length = integer("Вкажіть додатну довжину: ")
    first = rng.integers(0, 10, length, endpoint=True)
    second = rng.integers(10, 20, length, endpoint=True)
    print("Перший:", first, "Другий:", second)
    print("Об’єднання:", np.concatenate((first, second)))
    print("Додавання:", first + second)
    print("Різниця:", first - second)

    print("\n6. Зміна форми матриці")
    rows, columns = shape()
    matrix = np.arange(1, rows * columns + 1).reshape(rows, columns)
    print(matrix)
    print("Нова форма")
    matrix = matrix.reshape(shape(matrix.size))
    print(matrix)
    print("Мінімуми рядків:", matrix.min(axis=1))
    print("Максимуми рядків:", matrix.max(axis=1))
    print("Загальна сума:", matrix.sum())


if __name__ == "__main__":
    main()
