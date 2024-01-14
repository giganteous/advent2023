
from baseday import BaseDay
from collections import Counter, defaultdict



class Day02(BaseDay):
    games: dict[int, list[Counter]] = {}

    def init(self) -> None:
        """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"""
        with open(self.input) as fh:
            for line in fh.readlines():
                game, info = line.strip().split(': ')
                turns = []
                for turn in info.split('; '):
                    t = defaultdict(int) # default 0
                    for colorcount in turn.split(', '):
                        count, color = colorcount.split(' ')
                        t[color] = int(count)
                    turns.append(t)
                self.games[int(game.strip('Game '))] = turns

    def part1(self) -> None:
        """only 12 red cubes, 13 green cubes, and 14 blue cubes"""

        def is_impossible(grabs: list) -> bool:
            if any((max(t['red'] for t in grabs) > 12,
                    max(t['green'] for t in grabs) > 13,
                    max(t['blue'] for t in grabs) > 14)):
                return True

        validgames = 0
        for gameid, grabs in self.games.items():
            if is_impossible(grabs): continue
            validgames += gameid

        print(validgames)

    def part2(self) -> None:
        """What is the sum of the power of these sets?"""

        def maxpower(grabs: list) -> int:
            return max(t['red'] for t in grabs) * max(t['green'] for t in grabs) * max(t['blue'] for t in grabs)

        print(sum(maxpower(grabs) for _, grabs in self.games.items()))
