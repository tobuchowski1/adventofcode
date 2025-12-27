import sys


result = 0
data = []

for line in sys.stdin:
    line = line.strip()
    data.append([l for l in line.split(" ") if l != ""])

chars = data[-1]

for i, char in enumerate(chars):
    if char == '+':
        result += sum([int(line[i]) for line in data[:-1]])
    elif char == '*':
        partrial = 1
        for x in [int(line[i]) for line in data[:-1]]:
            partrial *= x
        result += partrial

print(result)

