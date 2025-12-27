import sys

sum = 0
ranges = []

for line in sys.stdin:
    line = line.strip()
    if line == "":
        break
    ranges.append(list(map(int, line.split('-'))))

ranges.sort()
current = [-1,-1]
for a,b in ranges:
    if a > current[1]:
        if current[0] != -1:
            sum += current[1] - current[0] + 1
        current = [a,b]
    else:
        current[1] = max(current[1], b)

sum += current[1] - current[0] + 1

print(sum)

# 333844603925511
# 342433357244012