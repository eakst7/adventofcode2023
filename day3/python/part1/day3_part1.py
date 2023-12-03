#!/usr/bin/env python3

import re


def readinput(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as fp:
        return fp.readlines()


def check_pos(pos: tuple[int, int], syms: dict[str, list[tuple[int, int]]]) -> str:
    for sym in syms:
        if pos in syms[sym]:
            return sym
    return None


def check_range(
    start: tuple[int, int], end: tuple[int, int], syms: dict[str, list[tuple[int, int]]]
) -> str:
    row = start[0]

    for col in range(start[1], end[1]):
        print((row, col))
        adjacent = find_adjacent((row, col))
        for x in adjacent:
            sym = check_pos(x, syms)
            if sym is not None:
                return sym

    return None


def find_adjacent(pos: tuple[int, int]) -> list[tuple[int, int]]:
    adjacent = []

    row = pos[0]
    col = pos[1]

    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            # print(f"Looking at ({r}, {c})")
            adjacent.append((r, c))

    return adjacent


def process(filename: str) -> int:
    syms: dict = {}
    input = readinput(filename)
    for row in range(len(input)):
        line = input[row].strip()
        for col in range(len(line)):
            sym = line[col]
            if not (sym.isdigit() or sym == "."):
                if syms.get(sym) is None:
                    syms[sym] = []
                syms[sym].append((row, col))

    total = 0
    for row in range(len(input)):
        line = input[row].strip()

        for m in re.finditer(r"(\d+)", line):
            value = int(m.group())
            start = (row, m.start())
            end = (row, m.end())
            print(f"{value} starts {start} ends {end}")
            if check_range(start, end, syms) is not None:
                total += value

    print(f"{total=}")
    return total


if __name__ == "__main__":
    process("input2.txt")

    # import re

    # line = '...654...721...'
    # for m in re.finditer('(\d+)', line):
    #     print(m)
    #     print(m.start())
    #     print(m.end())
    #     print(m.group())
