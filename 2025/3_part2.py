import sys

sum = 0


def calculate_voltage(data: str, n: int, acc: int = 0) -> int:
    if n == 0:
        return acc

    maxi = -1
    maxv = -1

    for i,d in enumerate(data[:-n]):
        if int(d) > maxv:
            maxv = int(d)
            maxi = i

    return calculate_voltage(data[maxi+1:], n-1, acc * 10 + maxv)

for line in sys.stdin:
    line = line.strip()
    sum += calculate_voltage(line + '$', 12)

print(sum)