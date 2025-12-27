import sys

sum = 0

data = []

for line in sys.stdin:
    line = line.strip()
    data.append(line)

moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
for i, line in enumerate(data):
    for j, val in enumerate(line):
        if val == '@':
            adjacent = 0
            for move in moves:
                if 0 <= move[0] + i < len(data) and 0 <= move[1] + j < len(line):
                    if data[move[0] + i][move[1] + j] == '@':
                        adjacent += 1
            if adjacent < 4:
                sum += 1

print(sum)