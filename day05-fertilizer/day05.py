from baseday import BaseDay
from dataclasses import dataclass
from itertools import islice
from math import ceil, log10
import sys
# Typing
from collections.abc import Iterator, Callable
import re

@dataclass(slots=True, frozen=False)
class Rule(object):
    dst: int
    src: int
    length: int
    def offset(self):
        return self.dst - self.src

@dataclass(slots=True, frozen=True)
class Seed(object):
    start: int
    length: int

def overlap(x1,x2,y1,y2) -> tuple[int, int] | None:
    start = max(x1, y1)
    end = min(x2, y2)
    if start <= end:
        return start, end
    return None

from typing import Self
@dataclass
class Converter(object):
    name: str
    rules: list[Rule]

    def lookup(self, v: int) -> int:
        for r in self.rules:
            if r.src <= v < r.src+r.length:
                # source hit => return destination + offset
                return v + (r.dst-r.src)
        # no mapping => source == destination
        return v

    def ilookup(self, v: int) -> int:
        """reverse of lookup"""
        for r in self.rules:
            if r.dst <= v < r.dst+r.length:
                print(f'(i) rule hit on {r}')
                return v + (r.src-r.dst)

    def reverserules(self, inp: Rule) -> list[Rule]:
        """
        Find the most optimal input for this converter to generate 
        any output in the requested range (start:start+length)
        """
        # all rules having overlap:
        s = [r for r in self.rules
                       if max(inp.src, r.dst) <= min(inp.src+inp.length, r.dst+r.length)]
        # sort by their lowest .dst.
        s = sorted(s, key=lambda y: y.dst)

        # fill gaps, and make copies
        g = []
        cutstart = inp.src
        cutend = (inp.src + inp.length)
        for e = s:
            if e.dst > cutstart:
                g.append(Rule(cutstart, e.dst-cutstart))

        # return rules (as ranges). fill in the gaps if there are gaps
        ret = []
        cutstart = inp.src
        cutend = (inp.src + inp.length)
        for e in s:
            if e.dst < cutstart:
                ret.append(Rule(e.src + (cutstart-e.dst), cutstart, e.length - e.
            elif e.dst > cutstart:
                print(f'>gap from {cutstart} to {e.dst}')
            print(f'rule from {e.dst} to {e.dst+e.length}')
            cutstart = e.dst + e.length
            if cutend < e.dst + e.length:
                e.length -= e.dst+e.length-cutend
                print(f'(updated) rule from {e.dst} to {e.dst+e.length}')

        # s[0] has the lowest dst; return lowest src giving a dst >= inp
        
        return s
    def max(self) -> Rule:
        return max(self.rules, key=lambda y: y.dst+y.length)
    def min(self) -> Rule:
        return min(self.rules, key=lambda y: y.dst)

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
                    allmaps[curmap]['rules'].append(Rule(dst, src, length))

        c = None
        for mapname, data in allmaps.items():
            c = Converter(name=data['name'], rules=data['rules'])
            self.converters.append(c)

    def part1(self) -> None:
        lookup = chained(list(x.lookup for x in self.converters))
        print(min(lookup(x) for x in self.seeds))

    def part2(self) -> None:
        lookup = chained(list(x.lookup for x in self.converters))

        converters = self.converters
        c = converters.pop()

        inp = Rule(src=0, length=10_000_000, dst=c.min())

        seeds = [Seed(a, b) for a,b in zip(self.seeds[::2], self.seeds[1::2])]
        def in_seed_range(rules: list[Rule]) -> list[tuple[int, int]]:
            overlaps = []
            for r in rules:
                for s in seeds:
                    x = is_overlapping(r.src, r.src+r.length, s.start, s.start+s.length)
                    if x != None:
                        overlaps.append((x[0], x[1]))
            return overlaps

        def followrules_to_seeds(rules, converters) -> list[tuple[int, int]]:
            if len(converters) == 0:
                return in_seed_range(rules)
            for r in rules:
                followuprules = converters[-1].reverserules(r)
                if followuprules:
                    return followrules_to_seeds(followuprules, converters[:-1])

        for r in c.reverserules(inp):
            overlap_with_seeds = followrules_to_seeds(r, converters)
            if len(overlap_with_seeds):
                print(f'rule {r} has overlaps with seeds: {overlap_with_seeds}')
