#!/usr/bin/env python3

from dataclasses import dataclass


input_data: str

@dataclass
class Node:
    l : str
    r : str

def readinput(filename: str):
    global input_data
    with open(filename, "r", encoding="utf-8") as fp:
        input_data = fp.read()

def process(filename: str) -> int:
    readinput(filename)

    input_lines: list[str] = input_data.split("\n")
    directions: str = input_lines[0]

    nodes: dict[str,Node] = {}
    for line in input_lines[2:]:
        (node, left, right) = (line[0:3], line[7:10], line[12:15])
        nodes[node] = Node(left, right)

    steps = 0
    n = "AAA"
    while n != "ZZZ":
        for d in directions:
            if d == "R":
                n = nodes[n].r
            else:
                n = nodes[n].l

            steps += 1

            if n == "ZZZ":
                break

    print(f"{steps=}")
    return steps


if __name__ == "__main__":
    process("input3.txt")
