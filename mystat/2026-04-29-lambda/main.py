if __name__ == "__main__":
    values = ["  hello ", "WORLD", " PyThOn  "]
    normalized = list(map(lambda value: value.strip().lower(), values))
    assert normalized == ["hello", "world", "python"]
    print(normalized)

    users = [{"name": "Іван", "age": 25}, {"name": "Оля", "age": 17}, {"name": "Петро", "age": 30}]
    names = sorted(
        map(lambda user: user["name"].upper(), filter(lambda user: user["age"] >= 18, users)),
        key=lambda name: len(name),
    )
    assert names == ["ІВАН", "ПЕТРО"]
    print(names)
