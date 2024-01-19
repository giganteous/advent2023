from baseday import BaseDay
import itertools
from collections.abc import Iterator
from typing import Tuple


class Day12(BaseDay):
    rows: list[str]

    def init(self) -> None:
        with open(self.input) as fh:
            self.rows = [x.strip() for x in fh.readlines()]

    def part1(self) -> None:
        # loop over all possibilities of ?, and see if
        # that could fit.

        def are_broken(s: str) -> Tuple[int, ...]:
            """.#...#....###. -> (1,1,3)"""
            return tuple(len(x) for x in s.split(".") if "#" in x)

        def options(s: str, totalcount: int, negcache: set) -> Iterator[str]:
            for x in itertools.product([".", "#"], repeat=s.count("?")):
                t = s.replace("?", "{}").format(*x)
                if t.count("#") != totalcount:
                    continue
                if t not in negcache:
                    yield t

        def split(s: str) -> Tuple[str, Tuple[int, ...]]:
            s, errors = s.split(" ")
            return (s, tuple(int(x) for x in errors.split(",")))

        def count_arrangements(springs: str) -> int:
            s, errors = split(springs)
            if self.example:
                print(s, errors)
            arrangements = 0
            ncache: set[str] = set()
            pcache: set[str] = set()
            for o in options(s, sum(errors), ncache):
                if o in ncache:
                    continue
                if o in pcache or are_broken(o) == errors:
                    arrangements += 1
                    pcache.add(o)
                else:
                    ncache.add(o)
            return arrangements

        print(sum(count_arrangements(x) for x in self.rows))

    def part2(self) -> None:
        pass  # Got stuck on a happy path. TBD
