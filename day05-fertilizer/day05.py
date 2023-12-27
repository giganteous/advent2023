from baseday import BaseDay
from dataclasses import dataclass
import collections.abc
#from typing import Tuple, Callable, Iterable
from itertools import islice

import re

# Itertools.batched from python3.12
def taketwo(iterable: collections.abc.Iterable) -> collections.abc.Iterator:
    # batched('ABCDEFG', 2) --> AB CD EF G
    it = iter(iterable)
    while batch := tuple(islice(it, 2)):
        yield batch

@dataclass
class Converter(object):
    name: str
    rules: list[tuple[int, int, int]]
    def addrule(self, rule: tuple[int, int, int]) -> None:
        self.rules.append(rule)
    def lookup(self, value: int) -> int:
        for dst, src, length in self.rules:
            if value >= src and value <= (src+length):
                # source hit => return destination + offset
                return dst + (value-src)
        # no mapping => source == destination
        return value

def chained(callables: list[collections.abc.Callable[[int], int]]) -> collections.abc.Callable[[int], int]:
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
                    rule = tuple(int(x) for x in line.strip().split())
                    allmaps[curmap]['rules'].append(rule)

        for mapname, data in allmaps.items():
            self.converters.append(Converter(name=data['name'], rules=data['rules']))

    def part1(self) -> None:
        lookup = chained(list(x.lookup for x in self.converters))
        print(min(lookup(x) for x in self.seeds))

    def part2(self) -> None:
        pass


