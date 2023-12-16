#!/usr/bin/env python3
# pylint: disable=global-statement
# pylint: disable=missing-docstring
# pylint: disable=multiple-statements

from enum import Enum
import numpy as np
from numpy.typing import NDArray
from icecream import ic

input_data: str
contraption: NDArray
energized: NDArray

class Dir(Enum):
    N: int = 0
    S: int = 1
    E: int = 2
    W: int = 3

def readinput(filename: str):
    global input_data
    with open(filename, "r", encoding="utf-8") as fp:
        input_data = fp.read()

type Pos = tuple[int,int]
type PosAndDir = tuple[Pos,Dir]

def up(p: Pos) -> Pos|None:
    r,c = p
    if r > 0:
        return (r-1,c)
    else:
        return None

def down(p: Pos) -> Pos|None:
    rows,_ = contraption.shape

    r,c = p
    if r < rows-1:
        return (r+1,c)
    else:
        return None

def left(p: Pos) -> Pos|None:
    r,c = p
    if c > 0:
        return (r,c-1)
    else:
        return None

def right(p: Pos) -> Pos|None:
    _,cols = contraption.shape

    r,c = p
    if c < cols-1:
        return (r,c+1)
    else:
        return None


def next_tiles(pos_and_dir: PosAndDir) -> PosAndDir:
    p, incoming_dir = pos_and_dir
    tile_type = contraption[p]
    match incoming_dir:
        case Dir.W:
            match tile_type:
                case ".":
                    next_tile = right(p)
                    if next_tile: return (next_tile, Dir.W)
                case "/":
                    next_tile = up(p)
                    if next_tile: return (next_tile, Dir.S)
                case "\\":
                    next_tile = down(p)
                    if next_tile: return (next_tile, Dir.N)
                case "-":
                    next_tile = right(p)
                    if next_tile: return (next_tile, Dir.W)
                case "|":
                    next_tile1 = up(p)
                    next_tile2 = down(p)
                    if next_tile1 and next_tile2:
                        beam = (next_tile2, Dir.N)
                        if beam not in beams:
                            beams.append(beam)
                        return (next_tile1, Dir.S)
                    if next_tile1: return (next_tile1, Dir.S)
                    if next_tile2: return (next_tile2, Dir.N)

        case Dir.E:
            match tile_type:
                case ".":
                    next_tile = left(p)
                    if next_tile: return (next_tile, Dir.E)
                case "/":
                    next_tile = down(p)
                    if next_tile: return (next_tile, Dir.N)
                case "\\":
                    next_tile = up(p)
                    if next_tile: return (next_tile, Dir.S)
                case "-":
                    next_tile = left(p)
                    if next_tile: return (next_tile, Dir.E)
                case "|":
                    next_tile1 = up(p)
                    next_tile2 = down(p)
                    if next_tile1 and next_tile2:
                        beam = (next_tile2, Dir.N)
                        if beam not in beams:
                            beams.append(beam)
                        return (next_tile1, Dir.S)
                    if next_tile1: return (next_tile1, Dir.S)
                    if next_tile2: return (next_tile2, Dir.N)

        case Dir.N:
            match tile_type:
                case ".":
                    next_tile = down(p)
                    if next_tile: return (next_tile, Dir.N)
                case "/":
                    next_tile = left(p)
                    if next_tile: return (next_tile, Dir.E)
                case "\\":
                    next_tile = right(p)
                    if next_tile: return (next_tile, Dir.W)
                case "|":
                    next_tile = down(p)
                    if next_tile: return (next_tile, Dir.N)
                case "-":
                    next_tile1 = right(p)
                    next_tile2 = left(p)
                    if next_tile1 and next_tile2:
                        beam = (next_tile2, Dir.E)
                        if beam not in beams:
                            beams.append(beam)
                        return (next_tile1, Dir.W)
                    if next_tile1: return (next_tile1, Dir.W)
                    if next_tile2: return (next_tile2, Dir.E)

        case Dir.S:
            match tile_type:
                case ".":
                    next_tile = up(p)
                    if next_tile: return (next_tile, Dir.S)
                case "/":
                    next_tile = right(p)
                    if next_tile: return (next_tile, Dir.W)
                case "\\":
                    next_tile = left(p)
                    if next_tile: return (next_tile, Dir.E)
                case "|":
                    next_tile = up(p)
                    if next_tile: return (next_tile, Dir.S)
                case "-":
                    next_tile1 = right(p)
                    next_tile2 = left(p)
                    if next_tile1 and next_tile2:
                        beam = (next_tile2, Dir.E)
                        if beam not in beams:
                            beams.append(beam)
                        return (next_tile1, Dir.W)
                    if next_tile1: return (next_tile1, Dir.W)
                    if next_tile2: return (next_tile2, Dir.E)

    return None

def follow_beam(pos_and_dir: PosAndDir):
    visited = set()
    current = pos_and_dir
    while current is not None and current not in visited:
        row,col = current[0]
        energized[row,col] += 1
        # ic(energized)
        visited.add(current)

        current = next_tiles(current)


beams: list[PosAndDir] = []

def calc_energy(pos_and_dir: PosAndDir):
    global beams, energized
    beams = []
    energized = np.zeros(contraption.shape)

    beams.append(pos_and_dir)
    i = 0
    while i < len(beams):
        # ic("Following beam", beams[i])
        follow_beam(beams[i])
        i += 1

    energy = 0
    for r in energized:
        for c in r:
            if c > 0:
                energy += 1

    return energy

def process(filename: str) -> int:
    global contraption

    readinput(filename)
    total: int = 0

    contraption = np.array([list(line) for line in input_data.strip().split("\n")])
    ic(contraption)

    tile = (0,0)
    direction = Dir.W

    total = calc_energy((tile, direction))

    print(f"{total=}")
    return total

if __name__ == "__main__":
    process("input2.txt")

