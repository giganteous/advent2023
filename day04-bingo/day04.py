from baseday import BaseDay
from dataclasses import dataclass
from collections import defaultdict

@dataclass(slots=True)
class Card(object):
    id: str
    winning: list[int]
    have: list[int]
    instances: int = 1
    def matching(self):
        return sum([x in self.winning for x in self.have])

    def score(self):
        score = 0
        for i in self.have:
            if i in self.winning:
                if score == 0:
                    score = 1
                else:
                    score *= 2
        return score

class Day04(BaseDay):
    cards: list[Card] = []

    def init(self):
        with open(self.input) as fh:
            for line in [x.strip() for x in fh.readlines()]:
                card, info = line.split(': ')
                winning, have = info.split(' | ')
                self.cards.append(Card(
                    int(card[5:]),
                    [int(x) for x in winning.split()],
                    [int(x) for x in have.split()],
                    1,
                ))
    def part1(self):
        print(sum(x.score() for x in self.cards))

    def part2(self):
        l = len(self.cards)
        for idx, c in enumerate(self.cards):
            score = c.matching()
            if self.example: print(f'we have {c.instances} cards of {c.id}. score={score}')
            for t in range(idx+1, min(idx+1+score, l)):
                self.cards[t].instances += c.instances
        print(sum(c.instances for c in self.cards))
