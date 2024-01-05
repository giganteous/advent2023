from baseday import BaseDay
from dataclasses import dataclass
from itertools import islice
from math import ceil, log10
import sys
# Typing
from collections.abc import Iterator, Callable
import re

@dataclass(slots=True, frozen=True)
class Range(object):
    start: int
    end: int
    offset: int


@dataclass(slots=True, frozen=True)
class Seed(object):
    start: int
    length: int

def overlap(x1,x2,y1,y2) -> tuple[int, int] | None:
    start = max(x1, y1)
    end = min(x2, y2)
    if start <= end:
        return start, end-start
    return None

def rangeoverlap(r1: Range, r2: Range, offset=0) -> Range | None:
    start = max(r1.start, r2.start)
    end = min(r1.end, r2.end)
    if start <= end:
        return Range(start, end, offset)
    return None

from typing import Self
@dataclass
class Converter(object):
    name: str
    rules: list[Range]

    def lookup(self, v: int) -> int:
        """single seed lookup"""
        for r in self.rules:
            if r.start <= v < r.end:
                return v + r.offset
        # no mapping => source == destination
        return v

    def rangelookup(self, inc: Range, invert=False) -> list[Range]:
        """lookups for range; return rewritten ranges"""
        destination = []
        for r in self.rules:
            o = rangeoverlap(inc, rule)
            if o is None: continue
            destination.append(Range(overlap.start+r.offset, overlap.end+r.offset, 0))
        return destination

def chained(callables: list[Callable[[int], int]]) -> Callable[[int], int]:
    def apply(x: int) -> int:
        for c in callables:
            x = c(x)
        return x
    return apply

class Day05(BaseDay):
    converters: list[Converter] = []
    seeds: list[int]

    def init(self) -> None:
        m = re.compile(r'^([a-z-]+) map:')
        allmaps = {} # type: ignore
        curmap = None
        with open(self.input) as fh:
            for line in fh.readlines():
                if line.startswith('seeds:'):
                    self.seeds = list(int(x) for x in line[6:].strip().split())
                    continue
                r = m.match(line)
                if r:
                    curmap = r.groups()[0]
                    allmaps[curmap] = {'name': curmap, 'rules': []}
                    continue
                if not line.strip():
                    curmap = None
                    continue
                if curmap:
                    dst, src, length = map(int, line.strip().split())
                    allmaps[curmap]['rules'].append(Range(src, src+length, dst-src))

        c = None
        for mapname, data in allmaps.items():
            c = Converter(name=data['name'], rules=data['rules'])
            self.converters.append(c)

    def part1(self) -> None:
        lookup = chained(list(x.lookup for x in self.converters))
        print(min(lookup(x) for x in self.seeds))

    def part2(self) -> None:
        for Range
