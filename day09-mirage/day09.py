from baseday import BaseDay
from itertools import pairwise

class Day09(BaseDay):
    data: list[list[int]] = []

    def init(self) -> None:
        with open(self.input) as fh:
            self.data = [[int(x) for x in line.strip().split()] for line in fh.readlines()]

    def part1old(self) -> None:
        total = 0
        for row in self.data:
            if self.example:
                print(f'row: {row}')
            while any(row):
                total += row[-1]
                row = [b - a for a, b in pairwise(row)]
                if self.example:
                    print(f'row: {row}')
        print(total)

    def part1(self) -> None:
        def recursive(x: list[int]) -> int:
            if any(x):
                return x[-1]+recursive([b-a for a,b in pairwise(x)])
            return 0
        print(sum(recursive(row) for row in self.data))

    def part2(self) -> None:
        def recursive(x: list[int]) -> int:
            if any(x):
                r = x[0]-recursive([b-a for a,b in pairwise(x)])
                return r
            return 0
        t = 0
        for row in self.data:
            r = recursive(row)
            t+=r

        print(t)
