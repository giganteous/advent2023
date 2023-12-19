from baseday import BaseDay
from PIL import Image, ImageDraw
import re
from typing import Tuple, List
m = re.compile('^(?P<direction>[RLDU]) (?P<length>[0-9]+) \((?P<rgb>[0-9a-f\#]{7})\)$')
class Day18(BaseDay):
    program: list[dict[str, str]] = []
    coords: List[Tuple[Tuple[int, int], str]] = []
    _offset: Tuple[int, int] = (0, 0)
    size: Tuple[int, int] = (0, 0)

    def init(self) -> None:
        with open(self.input) as fh:
            for line in fh.readlines():
                r = m.match(line)
                if r:
                    self.program.append(r.groupdict())
        self.parseprogram()

    def parseprogram(self) -> None:
        """enables fixup of .program, and re run this"""
        mn = (0, 0)
        mx = (0, 0)
        def update_minmax(c: Tuple[int, int]) -> None:
            nonlocal mn, mx
            mn = (min(mn[0], c[0]), min(mn[1], c[1]))
            mx = (max(mx[0], c[0]), max(mx[1], c[1]))

        x = y = 0
        for p in self.program:
            l = int(p['length'])
            if p['direction'] == 'R':
                x+=l
            elif p['direction'] == 'L':
                x-=l
            elif p['direction'] == 'U':
                y-=l
            elif p['direction'] == 'D':
                y+=l
            self.coords.append(((x, y), p['rgb']))
            if self.example: print(f'did {p}')
            update_minmax((x, y))
        print(f'image dimensions: {mn}, {mx}')

        self._offset = (-mn[0], -mn[1])
        print('offsets: ', self._offset[0], self._offset[1])

        # create image
        self.size = (mx[0]+self._offset[0]+1, mx[1]+self._offset[1]+1)
        print('size: ', self.size)

    def offset(self, oldc: Tuple[int, int]) -> Tuple[int, int]:
        return (oldc[0]+self._offset[0], oldc[1]+self._offset[1])

    def part1(self) -> None:
        image = Image.new("RGB", self.size, (255, 255, 255))
        draw = ImageDraw.Draw(image)
        black = '#ff0000'

        start = self.offset((0, 0))
        for end, color in ((self.offset(a), b) for a, b in self.coords):
            draw.line(start + end, fill='#00ff00')
            start = end
        middle = (self.size[0]/2, self.size[1]/2)
        #ImageDraw.floodfill(image, middle, (255,0,0))
        info = image.getcolors()
        #image.save('lagoon.png')
        print(sum(count for count, color in info if color != (255,255,255)))
        print(info)

    def part2(self) -> None:
        pass
