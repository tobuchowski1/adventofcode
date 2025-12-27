import sys
from queue import Queue

result = 0

for line in sys.stdin:
    line = line.strip()
    data = line.split(" ")
    start_pos = 0
    buttons = []
    for d in data:
        if d.startswith("["):
            for c in d.removesuffix(']').removeprefix('[')[::-1]:
                start_pos *= 2
                if c == '#':
                    start_pos += 1
        elif d.startswith("("):
            button = 0
            for n in d.removeprefix('(').removesuffix(')').split(','):
                button += pow(2,int(n))
            buttons.append(button)
    visited = set()
    q = Queue()
    q.put((0, start_pos))
    while not q.empty():
        depth, pos = q.get()
        if pos == 0:
            result += depth
            break
        for b in buttons:
            nextb = pos ^ b
            if nextb not in visited:
                visited.add(nextb)
                q.put((depth + 1, nextb))

print(result)

