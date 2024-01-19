from baseday import BaseDay
import string


class Day01(BaseDay):
    def example_value(self) -> int:
        return sum((12, 38, 15, 77))

    def part1(self) -> None:
        with open(self.input) as fh:
            data = fh.readlines()

        def firstandlast(s: str) -> int:
            if len(s):
                return int(s[0] + s[-1])
            return 0

        result = []
        for line in data:
            r = line.strip(string.ascii_lowercase + "\n")
            result.append(firstandlast(r))

        print("sum: ", sum(result))

    def part2(self) -> None:
        matches = {
            "0": 0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "eight": 8,
            "five": 5,
            "four": 4,
            "nine": 9,
            "one": 1,
            "seven": 7,
            "six": 6,
            "three": 3,
            "two": 2,
        }

        def firstandlast(s: str) -> int:
            if len(s):
                return int(first(s) + last(s))
            return 0

        def first(sentence: str) -> int:
            for s in range(0, len(sentence)):
                for i in matches.keys():
                    if sentence[s:].startswith(i):
                        # print(f"FIRST {sentence}: {i} => {matches[i]}")
                        return matches[i] * 10
            return 0

        def last(sentence: str) -> int:
            def idx(x: int) -> int | None:
                if x == 0:
                    return None
                return -1 * x

            for s in range(0, len(sentence)):
                for i in matches.keys():
                    if sentence[: idx(s)].endswith(i):
                        # print(f"LAST {sentence}: {i} => {matches[i]}")
                        return matches[i]
            return 0

        with open(self.input) as fh:
            data = fh.readlines()

        result = []
        for line in data:
            if self.example:
                print(f"line: {line}", end=None)
            result.append(firstandlast(line.strip("\n")))

        print("sum: ", sum(result))
