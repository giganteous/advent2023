from baseday import BaseDay

class Block():
    w = 0
    h = 0
    content = ''

    def __init__(self, w, h, content):
        self.w = w
        self.h = h
        self.content = content

    def row(self, i): # row1 == index[0]
        assert(i > 0 and i <= self.h)
        offset = (i-1) * self.w
        return self.content[offset:offset+self.w]
    def col(self, i):
        assert(i > 0 and i <= self.w)
        offset = i-1
        return self.content[offset::self.w]

    def scan_h(self):
        for a, b in zip(range(1, self.h), range(2, self.h+1)):
            if self.row(a) == self.row(b):
                # walk outward HEIGHT - min(a, b) steps
                size = min(a-1, self.h - b)
                if all(self.row(a-i) == self.row(b+i) for i in range(1, size+1)):
                    #print(f'h match on row {a} and {b}')
                    #print(self.row(a))
                    #print(self.row(b))
                    #print(f'walked outward {size} steps')
                    return a * 100
        return 0

    def scan_v(self):
        for a, b in zip(range(1, self.w), range(2, self.w+1)):
            if self.col(a) == self.col(b):
                size = min(a-1, self.w - b)
                if all(self.col(a-i) == self.col(b+i) for i in range(1, size+1)):
                    #print(f'v match on col {a} and {b}:')
                    #print(self.col(a))
                    #print(self.col(b))
                    #print(f'walked outward {size} steps')
                    return a
        return 0

class Day13(BaseDay):
    blocks: list[str]

    def init(self):
        with open(self.input) as fh:
            blocks = []
            width = height = 0
            content = []
            for line in (x.strip() for x in fh.readlines()):
                # new block
                if not line:
                    blocks.append(Block(width, height, ''.join(content)))
                    width = height = 0
                    content = []
                    #print()
                    continue
                #print(line)

                height+=1
                w = len(line)
                if not width:
                    width = w
                elif width != w:
                    print(f'weird length on {line}; C={content} w={width} h={height}')
                content.append(line)

            blocks.append(Block(width, height, ''.join(content)))
        self.blocks = blocks

    def part1(self):
        total = 0
        for b in self.blocks:
            total += b.scan_v()
            total += b.scan_h()
        print(total)

    def part2(self):
        # TBD

