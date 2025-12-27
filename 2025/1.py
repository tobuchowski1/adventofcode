import sys

pos = 50
zero_count = 0

for line in sys.stdin:
    line = line.strip()
    assert line[0] in 'LR'
    rotations = int(line.replace('L', '-').replace('R', '+'))
    pos = (pos + rotations) % 100
    if pos == 0:
        zero_count += 1
print(zero_count)