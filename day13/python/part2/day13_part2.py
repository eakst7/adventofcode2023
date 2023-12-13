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


def find_horizontal_reflection(lines: list[str], original: int):
    for (i,(l1,l2)) in enumerate(pairwise(lines)):
        if closematch(l1,l2):
            j = i
            k = i+1
            match = True
            while match and j >= 0 and k < len(lines):
                if not closematch(lines[j],lines[k]):
                    match = False
                else:
                    j -= 1
                    k += 1

            if match and original != (i+1):
                return i+1
    return -1

def find_original_horizontal_reflection(lines: list[str]):
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


def closematch(l1: str, l2: str) -> bool:
    if l1 == l2: return True

    mismatches = 0
    for (c1,c2) in zip(l1,l2):
        if c1 != c2:
            mismatches += 1
        if mismatches > 1:
            return False
    return True

def process(filename: str) -> int:
    readinput(filename)
    total: int = 0

    total_score = 0
    for pattern in input_data.split("\n\n"):
        print()
        print("Pattern:")
        print(pattern)

        lines = pattern.split("\n")
        flipped_lines = flip(lines)
        orig_horiz_score = find_original_horizontal_reflection(lines)
        orig_vert_score = find_original_horizontal_reflection(flipped_lines)

        horiz_score = find_horizontal_reflection(lines, orig_horiz_score)
        vert_score = find_horizontal_reflection(flipped_lines, orig_vert_score)

        print(f"Found original horizontal reflection at {orig_horiz_score}")
        print(f"Found original veritical reflection at {orig_vert_score}")
        print(f"Found horizontal reflection at {horiz_score}")
        print(f"Found veritical reflection at {vert_score}")
        if (horiz_score >= 0):
            total_score += (horiz_score * 100)
        elif (vert_score >= 0):
            total_score += vert_score


    print(f"{total_score=}")
    return total_score

if __name__ == "__main__":
    process("input2.txt")
    # ic(closematch("1234","1234"))
    # ic(closematch("1234","1245"))

