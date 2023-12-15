#!/usr/bin/env python3

input_data: str

def readinput(filename: str):
    global input_data
    with open(filename, "r", encoding="utf-8") as fp:
        input_data = fp.read()

def hash(s: str) -> int:
    current_value = 0
    for c in s:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256
    return current_value


def process(filename: str) -> int:
    readinput(filename)
    total: int = 0

    for step in input_data.split(","):
        total += hash(step)

    print(f"{total=}")
    return total

if __name__ == "__main__":
    process("input2.txt")
