#!/usr/bin/env python3

import re


def readinput(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as fp:
        return [line.strip() for line in fp.readlines()]


def process(filename: str) -> int:
    total: int = 0

    input_data = readinput(filename)

    count_by_card: dict[int,int] = {}

    for line in input_data:
        # print(f"{line}")
        r = re.split(r"\s+|:", line)
        # print(f"{r}")
        cardno = int(r[1])

        total_copies_of_this_card = count_by_card.get(cardno, 0) + 1
        count_by_card[cardno] = total_copies_of_this_card
        split_index = -1
        for i,v in enumerate(r):
            if v == '|':
                split_index = i
                break

        winning_numbers = r[3:split_index]
        my_numbers = r[(split_index)+1:]
        # print(f"{winning_numbers}")
        # print(f"{my_numbers}")

        matching_numbers = 0
        for n in my_numbers:
            if n in winning_numbers:
                matching_numbers += 1

        for i in range(1,matching_numbers+1):
            nextcardno = cardno + i
            count_by_card[nextcardno] = count_by_card.get(nextcardno, 0) + total_copies_of_this_card

    for key in count_by_card:
        total += count_by_card[key]

    print(f"{total=}")
    return total


if __name__ == "__main__":
    process("input2.txt")
    #process("input1.txt")