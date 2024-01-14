from baseday import BaseDay
from dataclasses import dataclass
from collections import defaultdict

@dataclass(slots=True)
class Card(object):
    matches: int = 0
    instances: int = 1

    def score(self):
        if not self.matches: return 0
        return 2**(self.matches-1)

class Day04(BaseDay):
    cards: list[Card] = []

    def init(self):
        with open(self.input) as fh:
            for line in [x.strip() for x in fh.readlines()]:
                card, info = line.split(': ')
                winning, have = info.split(' | ')
                self.cards.append(Card(
                    len(frozenset([int(x) for x in winning.split()])&
                    frozenset([int(x) for x in have.split()])),
                    1,
                ))
    def part1(self):
        print(sum(x.score() for x in self.cards))

    def part2(self):
        l = len(self.cards)
        for idx, c in enumerate(self.cards):
            for t in range(idx+1, min(idx+1+c.matches, l)):
                self.cards[t].instances += c.instances
        print(sum(c.instances for c in self.cards))
