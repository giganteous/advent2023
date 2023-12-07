from time import perf_counter

def timestr(secs: float) -> str:
    if secs == 0:
        return '0s'
    if secs < 0.001:
        return f"{secs * 1000000:.2f}us"
    if secs < 1:
        return f"{secs * 1000:.2f}ms"
    return f"{secs:.2f}s"

class BaseDay():
    input: str
    example: bool
    no_init: bool

    def __init__(self, input: str | None = None, example: bool = False):
        dir, name = self.__module__.split('.')
        if input is None:
            if example:
                input = dir + '/' + name + '-example.txt'
            else:
                input = dir + '/' + name + '-input.txt'
        self.input = input
        self.no_init = False

    def part1(self) -> None:
        raise NotImplementedError()

    def part2(self) -> None:
        raise NotImplementedError()

    def init(self) -> None:
        self.no_init = True

    def run(self, day: int, part: int | None = None) -> None:
        dt_init, dt_p1, dt_p2 = '-', '-', '-'

        t0 = perf_counter()
        self.init()
        if not self.no_init:
            dt_init = timestr(perf_counter() - t0)

        if part is None or part == 1:
            t0 = perf_counter()
            self.part1()
            dt_p1 = timestr(perf_counter() - t0)

        if part is None or part == 2:
            t0 = perf_counter()
            self.part2()
            dt_p2 = timestr(perf_counter() - t0)

        print(f"day{day:02} perf: init={dt_init}, part1={dt_p1}, part2={dt_p2}")
