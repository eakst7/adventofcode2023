#!/usr/bin/env python3

import numpy as np
from icecream import ic
from more_itertools import numeric_range

input_data: str

def readinput(filename: str):
    global input_data
    with open(filename, "r", encoding="utf-8") as fp:
        input_data = fp.read()

from numpy.typing import NDArray
def tilt_north(a: NDArray):
    (rows,cols) = a.shape
    for row in range(1,rows):
        for col in range(cols):
            if a[row,col] == "O":
                r = row-1
                while r >= 0 and a[r,col] == ".":
                    r -= 1
                if row > (r+1):
                    a[row][col] = "."
                    a[r+1][col] = "O"
                    # ic(a)

def tilt_west(a: NDArray):
    (rows,cols) = a.shape
    for col in range(1,cols):
        for row in range(rows):
            if a[row,col] == "O":
                c = col-1
                while c >= 0 and a[row,c] == ".":
                    c -= 1
                if col > (c+1):
                    a[row][col] = "."
                    a[row][c+1] = "O"


def tilt_south(a: NDArray):
    (rows,cols) = a.shape
    for row in numeric_range(rows-1, -1, -1):
        for col in range(cols):
            if a[row,col] == "O":
                r = row+1
                while r < rows and a[r,col] == ".":
                    r += 1
                if row < (r-1):
                    a[row][col] = "."
                    a[r-1][col] = "O"

def tilt_east(a: NDArray):
    (rows,cols) = a.shape
    for col in numeric_range(cols-1, -1, -1):
        for row in range(rows):
            if a[row,col] == "O":
                c = col+1
                while c < cols and a[row,c] == ".":
                    c += 1
                if col < (c-1):
                    a[row][col] = "."
                    a[row][c-1] = "O"

def process(filename: str) -> int:
    readinput(filename)
    total: int = 0

    a = np.array([list(line) for line in input_data.strip().split("\n")])
    ic(a)

    (rows,_) = a.shape

    tilt_north(a)

    ic(a)
    for (_,row) in enumerate(range(rows)):
        count = sum([1 for x in a[row] if x == 'O'])
        rows_below = rows - row

        total += rows_below * count


    print(f"{total=}")
    return total

if __name__ == "__main__":
    process("input2.txt")
