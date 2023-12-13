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

def closematch(a1: NDArray, a2: NDArray) -> bool:
    eq = np.equal(a1,a2)
    count = sum(1 for i in eq if not i)
    return count <= 1

def find_horizontal_reflection(a: NDArray, original: int):
    rows,_ = a.shape
    for (i,(r1,r2)) in enumerate(pairwise(a)):
        if closematch(r1,r2):
            j = i
            k = i+1
            
            match = True
            while match and j >= 0 and k < rows:
                if not closematch(a[j],a[k]):
                    match = False
                else:
                    j -= 1
                    k += 1

            if match and original != (i+1):
                return i + 1

    return -1

    # for (i,(l1,l2)) in enumerate(pairwise(lines)):
    #     if closematch(l1,l2):
    #         j = i
    #         k = i+1
    #         match = True
    #         while match and j >= 0 and k < len(lines):
    #             if not closematch(lines[j],lines[k]):
    #                 match = False
    #             else:
    #                 j -= 1
    #                 k += 1

    #         if match and original != (i+1):
    #             return i+1
    # return -1


def find_original_horizontal_reflection(a: NDArray):
    rows,_ = a.shape
    for (i,(r1,r2)) in enumerate(pairwise(a)):
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

        a = np.array([list(line) for line in pattern.split("\n")])

        flipped_a = a.T
        orig_horiz_score = find_original_horizontal_reflection(a)
        orig_vert_score = find_original_horizontal_reflection(flipped_a)

        horiz_score = find_horizontal_reflection(a, orig_horiz_score)
        vert_score = find_horizontal_reflection(flipped_a, orig_vert_score)

        # print(f"Found original horizontal reflection at {orig_horiz_score}")
        # print(f"Found original veritical reflection at {orig_vert_score}")
        # print(f"Found horizontal reflection at {horiz_score}")
        # print(f"Found veritical reflection at {vert_score}")
        if (horiz_score >= 0):
            total_score += (horiz_score * 100)
        elif (vert_score >= 0):
            total_score += vert_score

    print(f"{total_score=}")
    return total_score

if __name__ == "__main__":
    process("input2.txt")

