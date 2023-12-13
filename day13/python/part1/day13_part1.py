#!/usr/bin/env python3

from icecream import ic
from itertools import pairwise

input_data: str

def readinput(filename: str):
    global input_data
    with open(filename, "r", encoding="utf-8") as fp:
        input_data = fp.read()

def flip(lines: list[str]) -> list[str]:
    out: list[str] = []

    for c in range(len(lines[0])):
        outl = ""
        line = len(lines) - 1
        while (line >= 0):
            outl += lines[line][c]
            line -= 1
        out.append(outl)

    return out


def find_horizontal_reflection(lines: list[str]):
    for (i,(l1,l2)) in enumerate(pairwise(lines)):
        if l1 == l2:
            j = i
            k = i+1
            match = True
            while match and j >= 0 and k < len(lines):
                if lines[j] != lines[k]:
                    match = False
                else:
                    j -= 1
                    k += 1

            if match:
                return i+1
    return -1

def process(filename: str) -> int:
    readinput(filename)
    total: int = 0

    total_score = 0
    for pattern in input_data.split("\n\n"):
        print()
        print("Pattern:")
        print(pattern)

        lines = pattern.split("\n")
        horiz_score = find_horizontal_reflection(lines)
        if (horiz_score >= 0):
            print(f"Found horizontal reflection at {horiz_score}")
            total_score += (horiz_score * 100)

        vert_score = find_horizontal_reflection(flip(lines))
        if (vert_score >= 0):
            print(f"Found veritical reflection at {vert_score}")
            total_score += vert_score


    print(f"{total_score=}")
    return total_score

if __name__ == "__main__":
    process("input1.txt")

