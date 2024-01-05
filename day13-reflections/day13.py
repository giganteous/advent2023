from baseday import BaseDay
from itertools import pairwise


def cmp(ar1: str, ar2: str) -> int:
    return sum([x != y for x, y in zip(ar1, ar2)])


class Block:
    w = 0
    h = 0
    content = ""

    def __init__(self, w: int, h: int, content: str) -> None:
        self.w = w
        self.h = h
        self.content = content

    def row(self, i: int) -> str:  # row(1) == index[0]
        offset = (i - 1) * self.w
        return self.content[offset : offset + self.w]

    def col(self, i: int) -> str:
        offset = i - 1
        return self.content[offset :: self.w]

    def scan_h(self, maxdelta: int = 0) -> int:
        for a, b in pairwise(range(1, self.h + 1)):
            delta = cmp(self.row(a), self.row(b))
            if 0 <= delta <= maxdelta:
                size = min(a - 1, self.h - b)
                delta += sum(
                    cmp(self.row(a - i), self.row(b + i)) for i in range(1, size + 1)
                )
                if delta == maxdelta:
                    return a * 100
        return 0

    def scan_v(self, maxdelta: int = 0) -> int:
        for a, b in pairwise(range(1, self.w + 1)):
            delta = cmp(self.col(a), self.col(b))
            if 0 <= delta <= maxdelta:
                size = min(a - 1, self.w - b)
                delta += sum(
                    cmp(self.col(a - i), self.col(b + i)) for i in range(1, size + 1)
                )
                if delta == maxdelta:
                    return a
        return 0


class Day13(BaseDay):
    blocks: list[Block] = []

    def init(self) -> None:
        with open(self.input) as fh:
            width = height = 0
            content: list[str] = []
            for line in (x.strip() for x in fh.readlines()):
                # new block
                if not line:
                    self.blocks.append(Block(width, height, "".join(content)))
                    width = height = 0
                    content = []
                    # print()
                    continue
                if self.example:
                    print(line)

                height += 1
                w = len(line)
                if not width:
                    width = w
                elif width != w:
                    print(f"weird length on {line}; C={content} w={width} h={height}")
                content.append(line)

            self.blocks.append(Block(width, height, "".join(content)))

    def part1(self) -> None:
        total = 0
        for b in self.blocks:
            total += b.scan_v()
            total += b.scan_h()
        print(total)

    def part2(self) -> None:
        # TBD
        total = 0
        for b in self.blocks:
            total += b.scan_v(1)
            total += b.scan_h(1)
        print(total)
