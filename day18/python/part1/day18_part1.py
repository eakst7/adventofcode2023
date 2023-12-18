#!/usr/bin/env python3
# pylint: disable=global-statement
# pylint: disable=missing-docstring
# pylint: disable=multiple-statements

from icecream import ic # pylint: disable=unused-import

input_data: str

def readinput(filename: str):
    global input_data
    with open(filename, "r", encoding="utf-8") as fp:
        input_data = fp.read().strip()

def shoelace_area(points: list[tuple[int,int]]) -> int:
    # https://en.wikipedia.org/wiki/Shoelace_formula
    area = 0
    for i in range(0,len(points)-1):
        x1,y1 = points[i]
        x2,y2 = points[i+1]
        area += (x1*y2) - (x2*y1)

    x1,y1 = points[len(points)-1]
    x2,y2 = points[0]
    area += (x1*y2) - (x2*y1)

    return abs(area / 2)

def process(filename: str) -> int:
    readinput(filename)
    total: int = 0

    perimeter = 0
    points: list[tuple[int,int]] = []
    x,y = 0,0
    points.append((x,y))
    for line in input_data.split("\n"):
        (direction, meters, _) = line.split(" ")

        meters = int(meters)
        perimeter += meters
        match direction:
            case "R":
                x += meters
            case "L":
                x -= meters
            case "D":
                y -= meters
            case "U":
                y += meters

        points.append((x,y))

    ic(points)

    area = shoelace_area(points)

    # Pick's Theorem
    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    area = abs(area) + (perimeter / 2) + 1

    ic(area)

    print(f"{total=}")
    return total

if __name__ == "__main__":
    process("input1.txt")
