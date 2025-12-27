import sys

result = 0
split_count = 0
current_pos = set()
next_pos = set()

for line in sys.stdin:
    line = line.strip()
    for i, v in enumerate(line):
        if v == 'S':
            next_pos.add(i)
        if i not in current_pos or v != '^':
            continue
        split_count += 1
        next_pos.discard(i)
        if i > 0:
            next_pos.add(i - 1)
        if i < len(line) - 1:
            next_pos.add(i + 1)
    current_pos = next_pos.copy()

print(split_count)