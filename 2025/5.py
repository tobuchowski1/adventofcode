import sys

sum = 0

ranges = []

for line in sys.stdin:
    line = line.strip()
    if line == "":
        break
    ranges.append(list(map(int, line.split('-'))))

for line in sys.stdin:
    line = line.strip()
    number = int(line)
    for r in ranges:
        if r[0] <= number <= r[1]:
            sum += 1
            break

print(sum)