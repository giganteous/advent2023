from baseday import BaseDay
from itertools import combinations
from typing import Tuple
#from math import dist

class Day11(BaseDay):
    grid: list[list[bool]] = []
    expand_row: list[int] = []
    expand_col: list[int] = []

    def init(self) -> None:
        with open(self.input) as fh:
            for l in fh.readlines():
                self.grid.append([x == '#' for x in l.strip()])

        h = len(self.grid)
        w = len(self.grid[0])
        if self.example: print(f'grid dimension: w={w}, h={h}')
        for row in range(h):
            if not any(self.grid[row]):
                if self.example:
                    print(f'adding row at {row}')
                self.expand_row.append(row)
        for col in range(w):
            if not any([self.grid[x][col] for x in range(h)]):
                if self.example:
                    print(f'adding col at {col}')
                self.expand_col.append(col)

    def make_galaxies(self, factor) -> set[Tuple[int,int]]:
        galaxies: set[Tuple[int, int]] = set()
        for x in range(len(self.grid)):
            for y, has_galaxy in enumerate(self.grid[x]):
                if has_galaxy:
                    dx = dy = 0
                    for r in self.expand_row:
                        if x > r: dx+=factor
                    for c in self.expand_col:
                        if y > c: dy+=factor
                    galaxies.add((x+dx, y+dy))
        return galaxies

    @staticmethod
    def dist(a, b) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def part1(self) -> None:
        print(sum(self.dist(a, b) for a,b in combinations(self.make_galaxies(1), 2)))

    def part2(self) -> None:
        print(sum(self.dist(a, b) for a,b in combinations(self.make_galaxies(1_000_000 - 1), 2)))
