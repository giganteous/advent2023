from baseday import BaseDay
import re
import math
from typing import Iterable, Any


class Day08(BaseDay):
    directions: str
    maze: dict[str, list[str | Any]] = {}

    def init(self) -> None:
        with open(self.input) as fh:
            directions = fh.readline().strip()
            data = fh.readlines()

        m = re.compile(
            r"^(?P<here>[A-Z0-9]{3}) = \((?P<left>[A-Z0-9]{3}), (?P<right>[A-Z0-9]{3})\)"
        )
        for line in data:
            r = m.match(line.strip())
            if not r:
                continue
            self.maze[r.group("here")] = [r.group("left"), r.group("right")]
        self.directions = directions

    def route(self) -> Iterable:
        l = len(self.directions)
        i = [(x == "R") and 1 or 0 for x in self.directions]
        x = 0
        while True:
            yield i[x % l]
            x += 1

    def part1(self) -> None:
        we_are_at = "AAA"
        steps = 0
        for direction in self.route():
            if we_are_at == "ZZZ":
                break
            steps += 1
            we_are_at = self.maze[we_are_at][direction]

        print(f"part1: {steps}")

    def part2(self) -> None:
        starts = [x for x in self.maze.keys() if x.endswith("A")]
        ghoststeps = []
        for s in starts:
            steps = 0
            for direction in self.route():
                if s[2] != "Z":
                    break
                steps += 1
                s = self.maze[s][direction]

            # d = self.route()
            # steps = 0
            # while s[2] != 'Z':
            # direction = next(d)
            # steps += 1
            # s = self.maze[s][direction]
            ghoststeps.append(steps)
        print(f"part2: {math.lcm(*ghoststeps)}, number of ghosts: {len(starts)}")
