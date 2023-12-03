#!/usr/bin/env python3

import re


def readinput(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as fp:
        return fp.readlines()


def get_value_at(
    pos: tuple[int, int], nums: dict[tuple[int, int], tuple[tuple[int, int], int]]
) -> tuple[tuple[int, int], int]:
    row = pos[0]
    for startpos in nums:
        if row == startpos[0]:
            print(f"Checking row {row}")

            startcol = startpos[1]
            endcol = nums[startpos][0][1]

            r = range(startcol, endcol)
            print(f"  in range {r}")
            for col in range(startcol, endcol):
                if pos == (row, col):
                    return nums[startpos]

    return None


def find_adjacent(
    pos: tuple[int, int], nums: dict[tuple[int, int], tuple[tuple[int, int], int]]
) -> dict[tuple[int, int], int]:
    row = pos[0]
    col = pos[1]

    m: dict = {}
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            result = get_value_at((r, c), nums)
            if result is not None:
                (startpos, value) = result
                m[startpos] = value

    return m


def process(filename: str) -> int:
    nums: dict[tuple[int, int], tuple[tuple[int, int], int]] = {}
    input = readinput(filename)

    total = 0
    for row in range(len(input)):
        line = input[row].strip()

        for m in re.finditer(r"(\d+)", line):
            value = int(m.group())
            start = (row, m.start())
            end = (row, m.end())

            nums[start] = (end, value)

    for row in range(len(input)):
        line = input[row].strip()
        for m in re.finditer(r"\*", line):
            col = m.start()

            print(f"Looking around ({row},{col})")
            adjacent = find_adjacent((row, col), nums)

            gearratio = 0
            if len(adjacent) == 2:
                gearratio = 1
                for key in adjacent:
                    print(f"Found {adjacent[key]} at {key}")
                    gearratio *= adjacent[key]

            total += gearratio

    # print(nums)
    # print(get_value_at((0,0),nums))
    # print(get_value_at((2,2),nums))
    # print(get_value_at((2,3),nums))
    # print(get_value_at((1,1),nums))

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
