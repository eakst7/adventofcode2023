#!/usr/bin/env python3

import re


def readinput(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as fp:
        return [line.strip() for line in fp.readlines()]


def process(filename: str) -> int:
    total: int = 0

    input_data = readinput(filename)

    for line in input_data:
        # print(f"{line}")
        r = re.split(r"\s+|:", line)
        # print(f"{r}")
        # cardno = r[1]
        split_index = -1
        for i,v in enumerate(r):
            if v == '|':
                split_index = i
                break

        winning_numbers = r[3:split_index]
        my_numbers = r[(split_index)+1:]
        # print(f"{winning_numbers}")
        # print(f"{my_numbers}")

        card_score = 0
        for n in my_numbers:
            if n in winning_numbers:
                if card_score == 0:
                    card_score = 1
                else:
                    card_score *= 2

        total += card_score    

    print(f"{total=}")
    return total


if __name__ == "__main__":
    process("input2.txt")
