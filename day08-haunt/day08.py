from baseday import BaseDay
import re

import math

class Day08(BaseDay):
    directions: str
    maze: dict[tuple[str, str]]

    def init(self):
        with open(self.input) as fh:
            directions = fh.readline().strip()
            data = fh.readlines()

        maze: dict[tuple[str, str]] = {}
        m = re.compile(r'^(?P<here>[A-Z0-9]{3}) = \((?P<left>[A-Z0-9]{3}), (?P<right>[A-Z0-9]{3})\)')
        for line in data:
            r = m.match(line.strip())
            if not r:
                continue
            maze[r.group('here')] = [r.group('left'), r.group('right')]
        self.maze = maze
        self.directions = directions

    def route(self):
        l = len(self.directions)
        i = [(x == 'R') and 1 or 0 for x in self.directions]
        x = 0
        while True:
            yield i[x%l]
            x+=1

    def part1(self):
        d = self.route()

        we_are_at = 'AAA'
        steps = 0
        while we_are_at != 'ZZZ':
            steps += 1
            direction = next(d)
            we_are_at = self.maze[we_are_at][direction]

        print(f'part1: {steps}')

    def part2(self):
        starts = [ x for x in self.maze.keys() if x.endswith('A') ]
        ghoststeps = []
        for s in starts:
            d = self.route()
            steps = 0
            while s[2] != 'Z':
                direction = next(d)
                steps += 1
                s = self.maze[s][direction]
            ghoststeps.append(steps)
        print(f'part2: {math.lcm(*ghoststeps)}, number of ghosts: {len(starts)}')

