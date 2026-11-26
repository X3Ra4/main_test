from dataclasses import dataclass


@dataclass
class Money:
    whole: int = 0
    cents: int = 0
    currency: str = "UAH"

    def __post_init__(self):
        self.set_parts(self.whole, self.cents)

    def set_parts(self, whole, cents):
        if not isinstance(whole, int) or not isinstance(cents, int):
            raise TypeError("Вкажіть цілу кількість гривень та копійок")
        if whole < 0 or not 0 <= cents < 100:
            raise ValueError("Сума має бути невід’ємною, копійки від 0 до 99")
        self.whole, self.cents = whole, cents

    @property
    def minor_units(self):
        return self.whole * 100 + self.cents

    def __str__(self):
        return f"{self.whole}.{self.cents:02d} {self.currency}"

    def show(self):
        print(self)


@dataclass
class Product:
    name: str
    price: Money

    def reduce_price(self, discount):
        if self.price.currency != discount.currency:
            raise ValueError("Валюти ціни та знижки мають збігатися")
        amount = self.price.minor_units - discount.minor_units
        if amount < 0:
            raise ValueError("Знижка не може перевищити ціну")
        self.price = Money(*divmod(amount, 100), self.price.currency)


if __name__ == "__main__":
    product = Product("Блокнот", Money(120, 50))
    product.price.show()
    product.reduce_price(Money(15, 75))
    assert product.price.minor_units == 10475
    product.price.show()
