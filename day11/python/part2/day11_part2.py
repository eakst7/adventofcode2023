#!/usr/bin/env python3

from dataclasses import dataclass
from icecream import ic

input_data: str

@dataclass
class Node:
    galaxy: bool
    visited: bool
    distance: int

    def __repr__(self):
        return "#" if self.galaxy else "."

@dataclass
class Pos:
    row: int
    col: int

class Grid:
    table: list[list[Node]]

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
    
    def __setitem__(self, index: Pos|tuple[int,int], it: Node):
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
            self.table[r].append(None)
        self.table[r][c] = it

    def __str__(self):
        return self.table
    
    def _table(self):
        return self.table

    def rows(self) -> int:
        return len(self.table)
    
    def cols(self, row: int):
        return len(self.table[row])
    
    def insert_row(self, before_row: int, node: Node):
        if before_row >= len(self.table):
            cols = len(self.table[-1])
        else:
            cols = len(self.table[before_row])
        newrow: list[Node] = []
        for i in range(cols):
            newrow.append(node)
            
        self.table.insert(before_row, newrow)

    def insert_col(self, before_col: int, node: None):
        for row in self.table:
            if before_col >= len(row):
                row.append(node)
            else:
                row.insert(before_col, node)

    def get_neighbors(self, pos: Pos) -> list[Pos]:
        neighbors = []
        for r in range(pos.row - 1, pos.row + 2):
            for c in range(pos.col - 1, pos.col + 2):
                if not (r == pos.row and c == pos.col) \
                        and r >= 0 and c >= 0 \
                        and r < len(self.table) and c < len(self.table[r]):
                    neighbors.append(Pos(r,c))

        return neighbors


def get_distance(p1: Pos, p2: Pos, expando_rows: list[int], expando_cols: list[int]):
    row_start = min(p1.row, p2.row)
    row_end = max(p1.row, p2.row)
    row_dist = 0
    for i in range(row_start, row_end):
        if i in expando_rows:
            row_dist += 1000000
        else:
            row_dist += 1

    col_start = min(p1.col, p2.col)
    col_end = max(p1.col, p2.col)
    col_dist = 0
    for i in range(col_start, col_end):
        if i in expando_cols:
            col_dist += 1000000
        else:
            col_dist += 1

    return row_dist + col_dist

def readinput(filename: str):
    global input_data
    with open(filename, "r", encoding="utf-8") as fp:
        input_data = fp.read().strip()

def row_has_galaxy(grid: Grid, row: int) -> bool:
    for col in range(grid.cols(row)):
        if grid[(row,col)].galaxy:
            return True
        
    return False

def col_has_galaxy(grid: Grid, col: int) -> bool:
    for row in range(grid.rows()):
        if grid[(row,col)].galaxy:
            return True
        
    return False


def process(filename: str) -> int:
    readinput(filename)
    total: int = 0

    grid: Grid = Grid()
    galaxies: list[Pos] = []
    for r,line in enumerate(input_data .split("\n")):
        for c,it in enumerate(line):
            match it:
                case ".": grid[(r,c)] = Node(False, False, None)
                case "#":
                    grid[(r,c)] = Node(True, False, None)
                    galaxies.append(Pos(r,c))

    ic(grid._table())


    expando_rows: list[int] = []
    row = 0
    done = False

    while not done:
        if not row_has_galaxy(grid, row):
            expando_rows.append(row)
        row += 1

        if row >= grid.rows():
            done = True

    expando_cols: list[int] = []
    col = 0
    done = False

    while not done:
        if col >= grid.cols(0):
            done = True
        else:
            if not col_has_galaxy(grid, col):
                expando_cols.append(col)
            col += 1

    galaxies: list[Pos] = []
    for r in range(grid.rows()):
        for c in range(grid.cols(r)):
            if grid[(r,c)].galaxy:
                galaxies.append(Pos(r,c))

    distance_sum = 0
    for i1,g1 in enumerate(galaxies):
        for i2 in range(i1+1,len(galaxies)):
            g2 = galaxies[i2]
            dist_g1_g2 = get_distance(g1, g2, expando_rows, expando_cols)
            distance_sum += dist_g1_g2
            ic(i1,i2, dist_g1_g2)

    print(f"{distance_sum=}")
    return distance_sum

if __name__ == "__main__":
    process("input2.txt")
