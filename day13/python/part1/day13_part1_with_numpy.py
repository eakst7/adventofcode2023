#!/usr/bin/env python3

from itertools import pairwise

import numpy as np
from icecream import ic
from numpy.typing import NDArray

input_data: str

def readinput(filename: str):
    global input_data
    with open(filename, "r", encoding="utf-8") as fp:
        input_data = fp.read()

def find_horizontal_reflection(a: NDArray):
    ic(a)
    rows,_ = a.shape
    for (i,(r1,r2)) in enumerate(pairwise(a)):
        ic(i,r1,r2)
        if np.all(np.equal(r1,r2)):
            j = i
            k = i+1
            
            match = True
            while match and j >= 0 and k < rows:
                if not np.all(np.equal(a[j],a[k])):
                    match = False
                else:
                    j -= 1
                    k += 1

            if match:
                return i + 1

    return -1

def process(filename: str) -> int:
    readinput(filename)

    total_score = 0
    for pattern in input_data.split("\n\n"):
        pattern = pattern.strip()
        ic(pattern)

        a = np.array([list(line) for line in pattern.split("\n")])
        ic(a)
        ic(a.T)

        horiz_score = find_horizontal_reflection(a)
        if (horiz_score >= 0):
            print(f"Found horizontal reflection at {horiz_score}")
            total_score += (horiz_score * 100)

        vert_score = find_horizontal_reflection(a.T)
        if (vert_score >= 0):
            print(f"Found veritical reflection at {vert_score}")
            total_score += vert_score

    print(f"{total_score=}")
    return total_score

if __name__ == "__main__":
    process("input2.txt")
    # ic(closematch("1234","1234"))
    # ic(closematch("1234","1245"))

