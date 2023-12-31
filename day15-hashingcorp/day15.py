from baseday import BaseDay
from dataclasses import dataclass
from typing import Tuple
import re

m = re.compile(r'[-=]')

@dataclass
class Lens(object):
    label: str
    desc: str
    F: int
    def __repr__(self) -> str:
        return f'[{self.desc}]'


class Day15(BaseDay):
    data: str = ''

    def init(self) -> None:
        with open(self.input) as fh:
            self.steps = fh.read().strip().split(',')

    def part1(self) -> None:
        position = 0
        def hash(part: str) -> int:
            value = 0
            for position in range(len(part)):
                value += ord(part[position])
                value *= 17
                value %= 256
            return value

        total = 0
        for step in self.steps:
            total += hash(step)

        print(total)

    def part2(self) -> None:
        def hash(part: str) -> Tuple[int, Lens, bool]:
            """return focuspower,label and operation of the lens"""
            label, F = re.split(m, part)
            add = True
            if F == '':
                F = 0
                add = False

            h = 0
            for position in range(len(label)):
                h += ord(label[position])
                h *= 17
                h %= 256
            return h, Lens(label, f'{label} {F}', int(F)), add

        boxes: list[list[Lens]] = [[] for _ in range(256)]
        for step in self.steps:
            H, lens, add = hash(step)
            match = [b for b in boxes[H] if b.label == lens.label]
            if len(match):
                i = boxes[H].index(match[0])
                if add:
                    boxes[H][i] = lens
                else:
                    boxes[H].remove(match[0])
            elif add:
                boxes[H].append(lens)

        focuspower = 0
        for b in range(len(boxes)):
            if len(boxes[b]):
                if self.example:
                    print(f'Box {b}: {" ".join(str(x) for x in boxes[b])}')
                # calculate
                answer = (1+b)
                for x in range(len(boxes[b])):
                    Y = (1+b) * (x+1) * boxes[b][x].F
                    if self.example:
                        print(f'{boxes[b][x].label}: {b+1} (box {b}) * {x+1} ({x+1} slot) * {boxes[b][x].F} (focal length) = {Y}')
                    focuspower += Y
        #print()
        print(focuspower)
