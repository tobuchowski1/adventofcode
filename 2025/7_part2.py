import sys

result = 0
split_count = 0
current_pos = set()
next_pos = {}
possibilities = {}

for line in sys.stdin:
    line = line.strip()

    if len(possibilities) == 0:
        possibilities = {i: 0 for i in range(len(line))}
        next_pos = possibilities.copy()

    for i, v in enumerate(line):
        if v == 'S':
            next_pos[i] = 1
        if i not in possibilities or v != '^':
            continue
        next_pos[i] = 0
        if i > 0:
            next_pos[i - 1] += possibilities[i]
        if i < len(line) - 1:
            next_pos[i + 1] += possibilities[i]
    possibilities = next_pos.copy()

print(sum(possibilities.values()))

