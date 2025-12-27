import sys

sum = 0

data = []

for line in sys.stdin:
    line = line.strip()
    data.append([l for l in line])

moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

while True:
    partial = 0
    for i, line in enumerate(data):
        for j, val in enumerate(line):
            if val == '@':
                adjacent = 0
                for move in moves:
                    if 0 <= move[0] + i < len(data) and 0 <= move[1] + j < len(line):
                        if data[move[0] + i][move[1] + j] == '@':
                            adjacent += 1
                if adjacent < 4:
                    line[j] = 'x'
                    partial += 1
    sum += partial
    if partial == 0:
        break


print(sum)