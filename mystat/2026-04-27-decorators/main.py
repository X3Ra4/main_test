from datetime import datetime
from functools import wraps
from itertools import islice


def logger(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        print(f"[{datetime.now():%H:%M}] Викликано функцію {function.__name__}")
        return function(*args, **kwargs)
    return wrapped


def chunked(iterable, n):
    if n < 1:
        raise ValueError("Розмір чанка має бути додатним")
    iterator = iter(iterable)
    while chunk := list(islice(iterator, n)):
        yield chunk


@logger
def hello():
    return "Привіт!"


if __name__ == "__main__":
    print(hello())
    chunks = list(chunked(range(1, 6), 2))
    assert chunks == [[1, 2], [3, 4], [5]]
    for group in chunks:
        print(group)
