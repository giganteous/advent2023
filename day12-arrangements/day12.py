
from baseday import BaseDay
import itertools

class Day12(BaseDay):
    rows: list[str]

    def init(self):
        with open(self.input) as fh:
            self.rows=[ x.strip() for x in fh.readlines() ]

    def part1(self):
        # loop over all possibilities of ?, and see if 
        # that could fit.

        def are_broken(s: str):
            """ .#...#....###. -> (1,1,3)"""
            return tuple(len(x) for x in s.split('.') if '#' in x)

        def options(s: str):
            return (s.replace('?', '{}').format(*x) for x in list(itertools.product(['.', '#'], repeat=s.count('?'))))

        def split(s: str):
            s, errors = s.split(' ')
            return (s, tuple(int(x) for x in errors.split(',')))

        def count_arrangements(springs) -> int:
            s, errors = split(springs)
            #print(s, errors)
            arrangements = 0
            for o in options(s):
                if are_broken(o) == errors:
                    arrangements+=1
            return arrangements

        print(sum(count_arrangements(x) for x in self.rows))

    def part2(self):
        # Adding 4 questionmarks between the original
        # conditionrecords makes my implementation too slow.