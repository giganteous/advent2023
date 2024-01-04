from baseday import BaseDay
from typing import Optional, Tuple
import re
import functools
from collections import namedtuple
import math
Point = namedtuple('Point', ['x', 'y'])

wind = (
    (-1, -1), # ne
    (-1, 1),  # nw
    (-1, 0),  # n
    (0, 1),   # w
    (0, -1),  # e
    (1, 0),   # s
    (1, -1),  # se
    (1, 1),   # sw
)
nonsymbols = '0123456789.'
numfind = re.compile(r'([0-9]+)')

class Day03(BaseDay):
    def init(self) -> None:
        with open(self.input) as fh:
            self.data = [line.strip() for line in fh.readlines()]
            self.h = len(self.data)
            self.w = len(self.data[0])

    def part1(self) -> None:
        # build a map with numbers, and
        # a map with points that refer to the key of the numbers
        symbols: set[Point] = set()
        numbers: dict[Point, int] = {}
        p2n: dict[Point, Point] = {}
        for x, line in enumerate(self.data):
            for span in [x.span() for x in numfind.finditer(line)]:
                here = Point(x, span[0])
                for ny in range(span[0], span[1]):
                    p2n[Point(x, ny)] = here
                numbers[here] = int(line[span[0]:span[1]])
            for y in range(len(line)):
                if line[y] in nonsymbols: continue
                symbols.add(Point(x, y))

        uniq = set()
        for point in symbols:
            for dx, dy in wind: # adjacency
                if (point.x+dx, point.y+dy) in p2n:
                    uniq.add(p2n[Point(point.x+dx, point.y+dy)])

        print(sum([numbers[x] for x in uniq]))

    def part2(self) -> None:
        symbols: set[Point] = set()
        numbers: dict[Point, int] = {}
        p2n: dict[Point, Point] = {}
        for x, line in enumerate(self.data):
            for span in [x.span() for x in numfind.finditer(line)]:
                here = Point(x, span[0])
                for ny in range(span[0], span[1]):
                    p2n[Point(x, ny)] = here
                numbers[here] = int(line[span[0]:span[1]])
            map(symbols.add, [Point(x, y) for y in range(len(line)) if line[y] == '*' ])

        total = 0
        for point in symbols:
            two = set()
            for dx, dy in wind: # adjacency
                if (point.x+dx, point.y+dy) in p2n:
                    two.add(p2n[Point(point.x+dx, point.y+dy)])
            if len(two) == 2:
                total += math.prod([numbers[x] for x in two])

        print(total)

    # topaz.github.io: this never maps any numbers that have no overlap
    def part3(self) -> None:
        total = 0
        for x in range( self.h ):
            for y in range( self.w ):
                if self.data[ x ][ y ] != '*': continue

                parts = []
                for j in range( max( x - 1, 0 ), min( x + 2, self.h ) ):
                    start, end = y, y
                    while start > 0 and self.data[ j ][ start - 1 ].isdigit():
                        start -= 1
                    while end < self.w - 1 and self.data[ j ][ end + 1 ].isdigit():
                        end += 1
                    for num in [int(x) for x in numfind.findall(self.data[j][start:end+1])]:
                        parts.append(num)
                if len( parts ) == 2:
                    total += math.prod(parts)
        print(total)
