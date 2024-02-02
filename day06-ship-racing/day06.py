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
    def quadratic(a: int, b: int, c: int) -> tuple[float, float] | None:
        # calculate the value of X in "A*X**X + B*X + C = 0"
        D = b**2 - 4 * a * c
        # if D == 0, one answer.
        # if D < 0, no answers
        if D < 0:
            raise ValueError()
        root = math.sqrt(D)
        case1 = (-b + root) / (2 * a)
        case2 = (-b - root) / (2 * a)
        return case1, case2

    def ways(self) -> int:
        # ways to win the game. between the 2 times that
        # quadratic returns, inclusive.
        a, b = sorted(self.quadratic(-1, self.time, -self.win))

        # third, 30ms and 200mm:
        #  10.0-20.0: 20-10-1 => 9 (both 10 and 20 won't win)
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

    def part2(self) -> None:
        r = Race(
            int("".join(str(race.time) for race in self.races)),
            int("".join(str(race.win) for race in self.races)),
        )
        print(r.ways())
