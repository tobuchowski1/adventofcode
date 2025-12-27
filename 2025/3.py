import sys

sum = 0


for line in sys.stdin:
    line = line.strip()
    maxi = 0
    maxv = -1
    for i,d in enumerate(line[:-1]):
        if int(d) > maxv:
            maxv = int(d)
            maxi = i

    maxv2 = -1
    for j,d in enumerate(line[maxi+1:]):
        if int(d) > maxv2:
            maxv2 = int(d)
    sum += maxv * 10 + maxv2

print(sum)