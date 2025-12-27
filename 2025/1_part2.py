import sys

pos = 50
zero_count = 0

for line in sys.stdin:
    line = line.strip()
    assert line[0] in 'LR'
    rotations = int(line.replace('L', '-').replace('R', '+'))
    if not 0 < pos + rotations < 100:
        if pos == 0 and rotations < 0:
            zero_count -= 1
        zero_count += abs(pos + rotations) // 100
        if pos + rotations <= 0:
            zero_count += 1
    pos = (pos + rotations) % 100
print(zero_count)
