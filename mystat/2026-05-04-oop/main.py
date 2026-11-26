import argparse
from datetime import date
from math import gcd


class Person:
    def __init__(self, name, birth_date, phone, city, country, address):
        self._name = name
        self._birth_date = date.fromisoformat(birth_date) if isinstance(birth_date, str) else birth_date
        self._phone = phone
        self._city = city
        self._country = country
        self._address = address

    @property
    def name(self): return self._name

    @property
    def birth_date(self): return self._birth_date

    @property
    def phone(self): return self._phone

    @property
    def city(self): return self._city

    @property
    def country(self): return self._country

    @property
    def address(self): return self._address

    @classmethod
    def read(cls):
        labels = ["ПІБ", "Дата народження (РРРР-ММ-ДД)", "Телефон", "Місто", "Країна", "Адреса"]
        return cls(*(input(f"{label}: ").strip() for label in labels))

    def __str__(self):
        return f"{self.name}, {self.birth_date}; {self.phone}; {self.country}, {self.city}, {self.address}"

    def show(self):
        print(self)


class Fraction:
    def __init__(self, numerator, denominator):
        if denominator == 0:
            raise ZeroDivisionError("Знаменник не може дорівнювати нулю")
        common = gcd(numerator, denominator)
        sign = 1 if denominator > 0 else -1
        self._numerator = sign * numerator // common
        self._denominator = abs(denominator) // common

    @property
    def numerator(self): return self._numerator

    @property
    def denominator(self): return self._denominator

    @classmethod
    def read(cls):
        return cls(int(input("Чисельник: ")), int(input("Знаменник: ")))

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

    def show(self):
        print(self)

    def __add__(self, other):
        return Fraction(self.numerator * other.denominator + other.numerator * self.denominator,
                        self.denominator * other.denominator)

    def __sub__(self, other):
        return self + Fraction(-other.numerator, other.denominator)

    def __mul__(self, other):
        return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)

    def __truediv__(self, other):
        return self * Fraction(other.denominator, other.numerator)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--interactive", action="store_true")
    args = parser.parse_args()
    person = Person.read() if args.interactive else Person("Олена Тест", "2000-04-12", "000", "Дніпро", "Україна", "Приклад 1")
    person.show()
    first, second = (Fraction.read(), Fraction.read()) if args.interactive else (Fraction(1, 2), Fraction(2, 3))
    for symbol, result in [("+", first + second), ("−", first - second), ("×", first * second), ("÷", first / second)]:
        print(f"{first} {symbol} {second} = {result}")
