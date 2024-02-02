from baseday import BaseDay
from dataclasses import dataclass
import math
from functools import reduce
from operator import mul


@dataclass
class Race(object):
    time: int = 0
    win: int = 0

    @staticmethod
    def quadratic(a: int, b: int, c: int) -> tuple[float, float]:
        root = math.sqrt(b**2 - 4 * a * c)
        case1 = (-b + root) / 2 * a
        case2 = (-b - root) / 2 * a
        return case1, case2

    def ways(self) -> int:
        # ways to win the game. between the 2 times that
        # quadratic returns, inclusive.
        a, b = sorted(self.quadratic(-1, self.time, -self.win))

        # first testrace: 2,3,4 and 5 are winning; 5-2+1
        return math.ceil(b) - math.floor(a) - 1


class Day06(BaseDay):
    races: list[Race] = []

    def init(self) -> None:
        with open(self.input) as fh:
            # Times:    t0 t1 t2
            # Distance: d0 d1 d2
            times = fh.readline().strip().split()[1:]
            distances = fh.readline().strip().split()[1:]
            for t, d in zip(times, distances):
                self.races.append(Race(int(t), int(d)))

    def part1(self) -> None:
        races = [race.ways() for race in self.races]
        print(reduce(mul, races))

    def part2a(self) -> None:
        r = Race(
            int("".join(str(race.time) for race in self.races)),
            int("".join(str(race.win) for race in self.races)),
        )
        print(r.ways())
