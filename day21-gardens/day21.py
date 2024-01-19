from baseday import BaseDay
from collections import namedtuple
from itertools import pairwise

Point = namedtuple("Point", ["x", "y"])


class Day21(BaseDay):
    def init(self) -> None:
        with open(self.input) as fh:
            self.map = [[x for x in line.strip()] for line in fh.readlines()]
        self.h = len(self.map)  # x
        self.w = len(self.map[0])  # y

    def find_s(self) -> Point:
        for y, line in enumerate(self.map):
            if "S" in line:
                return Point(line.index("S"), y)
        raise ValueError()

    def printmap(self, rightnow: set = set()) -> None:
        c = [row.copy() for row in self.map]
        for p in rightnow:
            c[p.x][p.y] = "O"
        for row in c:
            print("".join(row))

    def possibilities(self, p: Point, steps: int) -> None:
        def move_once(source: set[Point]) -> set[Point]:
            dest = set()
            for p in source:
                for dx, dy in (
                    (p.x, p.y - 1),
                    (p.x, p.y + 1),
                    (p.x - 1, p.y),
                    (p.x + 1, p.y),
                ):
                    if any(
                        (
                            dx < 0,
                            dx > self.h,
                            dy < 0,
                            dy > self.w,
                            self.map[dx][dy] != ".",
                        )
                    ):
                        continue
                    dest.add(Point(dx, dy))
            return dest

        series = []
        reach = set([p])
        for i in range(steps):
            series.append(len(reach))
            reach = move_once(reach)

            if self.example:
                self.printmap(reach)
        print(len(reach))

    def part1(self) -> None:
        start = self.find_s()
        self.map[start.x][start.y] = "."  # it is a garden step
        if self.example:
            self.printmap()
        steps = 64
        if self.example:
            steps = 6
        self.possibilities(start, steps)

    def part2(self) -> None:
        pass
