from functools import wraps


def generator_logger(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        for item in function(*args, **kwargs):
            print(f"[LOG] Yield: {item}")
            yield item
    return wrapped


@generator_logger
def numbers(count):
    yield from range(count)


if __name__ == "__main__":
    received = []
    for number in numbers(3):
        print(f"Received: {number}")
        received.append(number)
    assert received == [0, 1, 2]
