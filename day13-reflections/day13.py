from baseday import BaseDay
from itertools import pairwise

class Block():
    w = 0
    h = 0
    content = ''

    def __init__(self, w: int, h: int, content: str) -> None:
        self.w = w
        self.h = h
        self.content = content

    def row(self, i: int) -> str: # row(1) == index[0]
        offset = (i-1) * self.w
        return self.content[offset:offset+self.w]

    def col(self, i: int) -> str:
        offset = i-1
        return self.content[offset::self.w]

    def scan_h(self) -> int:
        for a, b in pairwise(range(1, self.h+1)):
            if self.row(a) == self.row(b):
                size = min(a-1, self.h - b)
                if all(self.row(a-i) == self.row(b+i) for i in range(1, size+1)):
                    return a * 100
        return 0

    def scan_v(self) -> int:
        for a, b in pairwise(range(1, self.w+1)):
            if self.col(a) == self.col(b):
                size = min(a-1, self.w - b)
                if all(self.col(a-i) == self.col(b+i) for i in range(1, size+1)):
                    return a
        return 0

class Day13(BaseDay):
    blocks: list[Block]

    def init(self) -> None:
        with open(self.input) as fh:
            width = height = 0
            content: list[str] = []
            for line in (x.strip() for x in fh.readlines()):
                # new block
                if not line:
                    self.blocks.append(Block(width, height, ''.join(content)))
                    width = height = 0
                    content = []
                    #print()
                    continue
                if self.example:
                    print(line)

                height+=1
                w = len(line)
                if not width:
                    width = w
                elif width != w:
                    print(f'weird length on {line}; C={content} w={width} h={height}')
                content.append(line)

            self.blocks.append(Block(width, height, ''.join(content)))

    def part1(self) -> None:
        total = 0
        for b in self.blocks:
            total += b.scan_v()
            total += b.scan_h()
        print(total)

    def part2(self) -> None:
        # TBD
        pass
