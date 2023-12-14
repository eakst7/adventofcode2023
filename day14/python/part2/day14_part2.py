#!/usr/bin/env python3

import time
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

    (rows,_) = a.shape

    prev = []
    starttime = time.time()
    for cycle in range(1000000000):
        prev.append(np.copy(a))

        if (cycle % 1000) == 0:
            elapsed_time = time.time() - starttime
            ic(elapsed_time, cycle, cycle/elapsed_time)

        tilt_north(a)
        tilt_west(a)
        tilt_south(a)
        tilt_east(a)

        for (i,p) in enumerate(prev):
            if np.all(a == p):
                print(f"Found a cycle from {i} to {cycle}")
                cyclelen = cycle - i

                cycles_remaining = (1_000_000_000 - cycle)
                x = int(cycles_remaining / cyclelen)
                w = x * cyclelen
                additional_cyles = cycles_remaining - w

                for i in range(additional_cyles):
                    tilt_north(a)
                    tilt_west(a)
                    tilt_south(a)
                    tilt_east(a)

                for (_,row) in enumerate(range(rows)):
                    count = sum([1 for x in a[row] if x == 'O'])
                    rows_below = rows - row

                    total += rows_below * count
                break

        if total > 0:
            break

    print(f"{total=}")
    return total

if __name__ == "__main__":
    process("input2.txt")
