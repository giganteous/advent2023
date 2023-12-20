from baseday import BaseDay
from PIL import Image, ImageDraw
import re
from collections import namedtuple
from typing import Tuple

Point = namedtuple('Point', ['x', 'y'])
Directive = namedtuple('Directive', ['dir', 'dist'])

m = re.compile('^(?P<dir>[RLDU]) (?P<dist>[0-9]+) \((?P<rgb>[0-9a-f\#]{7})\)$')
class Day18(BaseDay):
    colors: list[str] = []
    program: list[Directive] = []

    def init(self) -> None:
        with open(self.input) as fh:
            for line in fh.readlines():
                r = m.match(line)
                if r:
                    x = r.groupdict()
                    self.program.append(Directive(x['dir'], int(x['dist'])))
                    self.colors.append(x['rgb'])

    @staticmethod
    def move(coord: Point, direction: int, dist: int) -> Point:
        # 0 -> x+=N; 1 -> y+=N; 2 -> x-=N; 3 -> y-=N;
        match (coord, direction, dist):
            case ((x, y), 0 | 'R', l):
                return Point(x+l, y)
            case ((x, y), 1 | 'D', l):
                return Point(x, y+l)
            case ((x, y), 2 | 'L', l):
                return Point(x-l, y)
            case ((x, y), 3 | 'U', l):
                return Point(x, y-l)
        print(coord, direction, dist)
        raise ValueError()


    def part1(self) -> None:
        coords = []
        start = Point(0, 0)
        for p in self.program:
            dest = self.move(start, p.dir, p.dist)
            coords.append(dest)
            start = dest
            if self.example: print(f'{p} -> {dest}')

        mn = Point(min(p.x for p in coords), min(p.y for p in coords))
        mx = Point(max(p.x for p in coords), max(p.y for p in coords))

        def offset(p: Point) -> Point:
            return Point(p.x-mn.x, p.y+mn.y)
        size = Point(mx.x-mn.x+1, mx.y-mn.y+1)

        if self.example:
            print(f'min/max: {mn}, {mx}')
            print(f'image dimensions: {mn}, {mx}')
            print('offsets: ', -mn.x, -mn.y)
            print('size: ', size)

        # create image
        image = Image.new("RGB", size, (255, 255, 255))
        draw = ImageDraw.Draw(image)

        start = Point(-mn.x, -mn.y)
        for end in (offset(a) for a in coords):
            draw.line(start + end, fill=(0,255,0))
            start = end
        middle = (size.x/2, size.y/2)
        ImageDraw.floodfill(image, middle, (255,0,0))
        info = image.getcolors()
        if self.example:
            print(info)
        image.save('lagoon.png')
        print(sum(count for count, color in info if color != (255,255,255)))


    def part2(self) -> None:
        def shoelace(alist: list[Point], total_distance: int) -> int:
            s1 = sum(a.x*b.y for a, b in zip(alist, alist[1:]))
            s2 = sum(a.x*b.y for a, b in zip(alist[1:], alist))

            # points within the boundary; Picks Theorem
            interior = (s1 - s2) / 2 - (total_distance/2) + 1

            # add the points under the boundary itself
            return int(interior) + total_distance

        def fixup(rgb: str) -> Directive:
            return Directive(int(rgb[6]), int(rgb[1:6], base=16))
        #, int(rgb[6])

        start = Point(0, 0)
        coords: list[Point] = [start]
        circumference = 0
        for color in self.colors:
            direction, dist = fixup(color)
            circumference += dist
            dest = self.move(start, direction, dist)
            coords.append(dest)
            start = dest

        print(shoelace(coords, circumference))
