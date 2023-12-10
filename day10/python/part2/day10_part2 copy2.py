#!/usr/bin/env python3

from multiprocessing import Pool
from dataclasses import dataclass
from enum import Enum
from sympy.geometry import Polygon
from icecream import ic

input_data: str

type RowNum = int
type ColNum = int

@dataclass
class Pos:
    row: int
    col: int

class Dir(Enum):
    N = 0
    S = 1
    E = 2
    W = 3

def flip(d: Dir) -> Dir:
    match d:
        case Dir.N:
            return Dir.S
        case Dir.S:
            return Dir.N
        case Dir.E:
            return Dir.W
        case Dir.W:
            return Dir.E

class Pipe(Enum):
    VT = (Dir.N,Dir.S) # | Vertical
    HZ = (Dir.W,Dir.E) # - Horizontal
    NE = (Dir.N,Dir.E) # L North and East
    NW = (Dir.N,Dir.W) # J North and West
    SW = (Dir.S,Dir.W) # 7 South and West
    SE = (Dir.S,Dir.E) # F South and East
    GR = (None,None) # . Ground
    ST = () # S Start

    def outdir(self, indir: Dir) -> Dir:
        return self.value[0] if indir == self.value[1] else self.value[1] # type: ignore

    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        match self:
            case Pipe.VT: return "VT"
            case Pipe.HZ: return "HZ"
            case Pipe.NE: return "NE"
            case Pipe.NW: return "NW"
            case Pipe.SW: return "SW"
            case Pipe.SE: return "SE"
            case Pipe.GR: return "GR"
            case Pipe.ST: return "ST"





class Grid:
    table: list[list[Pipe]]

    def __init__(self):
        self.table = []

    def __getitem__(self, index: Pos|tuple[int,int]):
        if isinstance(index, tuple):
            r = index[0]
            c = index[1]
        elif isinstance(index, Pos):
            r = index.row
            c = index.col

        return self.table[r][c]
    
    def __setitem__(self, index: Pos|tuple[int,int], it: Pipe):
        if isinstance(index, tuple):
            r = index[0]
            c = index[1]
        elif isinstance(index, Pos):
            r = index.row
            c = index.col

        for i in range(len(self.table), r+1):
            self.table.append([])
        row = self.table[r]
        for i in range(len(row), c+1):
            self.table[r].append(Pipe.GR)
        self.table[r][c] = it

    def __str__(self):
        return self.table
    
    def _table(self):
        return self.table

    def rows(self) -> int:
        return len(self.table)
    
    def cols(self, row: int):
        return len(self.table[row])

def readinput(filename: str):
    global input_data
    with open(filename, "r", encoding="utf-8") as fp:
        input_data = fp.read().strip()

def find_start(grid: Grid) -> Pos:
    for r in range(grid.rows()):
        for c in range(grid.cols(r)):
            if grid[(r,c)] == Pipe.ST:
                return Pos(r,c)
            
    return Pos(-1,-1)

def determine_start_shape(grid: Grid, start: Pos) -> Pipe:
    north: Pos = Pos(start.row-1,start.col)
    south: Pos = Pos(start.row+1,start.col)
    west: Pos = Pos(start.row, start.col-1)
    east: Pos = Pos(start.row, start.col+1)

    connected_north = True if grid[north] in (Pipe.VT, Pipe.SW, Pipe.SE) else False
    connected_south = True if grid[south] in (Pipe.VT, Pipe.NW, Pipe.NE) else False

    connected_east = True if grid[east] in (Pipe.HZ, Pipe.NW, Pipe.SW) else False
    connected_west = True if grid[west] in (Pipe.HZ, Pipe.NE, Pipe.SE) else False

    if connected_north and connected_south: return Pipe.VT
    if connected_north and connected_west: return Pipe.NW
    if connected_north and connected_east: return Pipe.NE
    if connected_south and connected_west: return Pipe.SW
    if connected_south and connected_east: return Pipe.SE
    if connected_west and connected_east: return Pipe.HZ

    assert False

def advance(grid: Grid, pos: Pos, direction: Dir) -> tuple[Pos,Dir]:

    match direction:
        case Dir.N:
            next_pos = Pos(pos.row-1, pos.col)
        case Dir.S:
            next_pos = Pos(pos.row+1, pos.col)
        case Dir.E:
            next_pos = Pos(pos.row, pos.col+1)
        case Dir.W:
            next_pos = Pos(pos.row, pos.col-1)
        
    next_pipe = grid[next_pos]
    next_dir = next_pipe.outdir(flip(direction))
    
    return (next_pos, next_dir)


    assert False

def follow(grid: Grid, start_pos: Pos) -> list[Pos]:
    points: Pos = [start_pos]
    current_pos = start_pos
    direction: Dir = grid[start_pos].value[0] # type: ignore
    (current_pos, direction) = advance(grid,current_pos, direction)
    while (current_pos != start_pos):
        points.append(current_pos)
        (current_pos,direction) = advance(grid, current_pos, direction)

    return points


def process(filename: str) -> int:
    readinput(filename)

    grid: Grid = Grid()
    for r,line in enumerate(input_data .split("\n")):
        for c,it in enumerate(line):
            match it:
                case "|": grid[(r,c)] = Pipe.VT
                case "-": grid[(r,c)] = Pipe.HZ
                case "L": grid[(r,c)] = Pipe.NE
                case "J": grid[(r,c)] = Pipe.NW
                case "7": grid[(r,c)] = Pipe.SW
                case "F": grid[(r,c)] = Pipe.SE
                case ".": grid[(r,c)] = Pipe.GR
                case "S": grid[(r,c)] = Pipe.ST

    #ic(grid._table())
    st_pos = find_start(grid)
    st_shp = determine_start_shape(grid, st_pos)
    grid[st_pos] = st_shp

    points = follow(grid, st_pos)

    points = [(x.row,x.col) for x in points]
    #ic(points)

    poly = Polygon(*points)
    #ic(poly)

    enclosed = 0
    coords = []
    for r,line in enumerate(input_data .split("\n")):
        for c,it in enumerate(line):
            coords.append((r,c))

    import functools

    f = functools.partial(check, poly)
    with Pool(16) as p:
        r = p.map(f, coords)
        for x in r:
            if x:
                enclosed += 1


    print(f"{enclosed=}")
    return enclosed

def check(poly: Polygon, point: tuple[int,int]):
    print(f"Checking {point[0]},{point[1]}")
    r = poly.encloses_point(point)
    print(f"Checked {point[0]},{point[1]} {r}")
    return r

if __name__ == "__main__":
    process("input4.txt")
