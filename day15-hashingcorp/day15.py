from baseday import BaseDay
from collections import namedtuple
from typing import NamedTuple
import re

class Lens(NamedTuple):
    label: str = ''
    desc: str = ''
    F: int = 0

    def __repr__(self):
        return f'[{self.desc}]'

m = re.compile(r'[-=]')

class Day15(BaseDay):
    data: str = ''

    def init(self):
        with open(self.input) as fh:
            self.steps = fh.read().strip().split(',')

    def part1(self):
        total = 0
        position = 0
        def hash(part: str) -> int:
            value = 0
            for position in range(len(part)):
                value += ord(part[position])
                value *= 17
                value %= 256
            return value

        for step in self.steps:
            become = hash(step)
            print(f'{step} becomes {become}.')
            total += become

        print(total)

    def part2(self):
        def hash(part: str) -> (int, str, bool):
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

        boxes = []
        for i in range(256): boxes.append([])
        for step in self.steps:
            H, lens, add = hash(step)
            match = [b for b in boxes[H] if b.label == lens.label]
            i = None
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
                #print(f'Box {b}: {" ".join(str(x) for x in boxes[b])}')
                # calculate
                answer = (1+b)
                for x in range(len(boxes[b])):
                    Y = (1+b) * (x+1) * boxes[b][x].F
                    #print(f'{boxes[b][x].label}: {b+1} (box {b}) * {x+1} ({x+1} slot) * {boxes[b][x].F} (focal length) = {Y}')
                    focuspower += Y
        #print()
        print(focuspower)
