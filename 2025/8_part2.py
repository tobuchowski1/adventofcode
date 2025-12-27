import math
import sys
from dataclasses import dataclass

CONNECTIONS_COUNT = 1000

@dataclass
class Point:
    x: int
    y: int
    z: int

def distance(a: Point, b: Point) -> float:
    return math.sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2) + pow(a.z - b.z, 2))

points = []

for line in sys.stdin:
    line = line.strip()
    points.append(Point(*map(int, line.split(','))))

distances = []

sys.stdin = open("/dev/tty")

for i, p1 in enumerate(points):
    for j, p2 in enumerate(points[i+1:]):
        distances.append((distance(p1, p2), (i,i+j+1)))

distances.sort()
R = list(range(len(points)))

def repr(i: int) -> int:
    if R[i] == i:
        return i
    R[i] = repr(R[i])
    return R[i]

group_count = len(points)

for d in distances:
    r1 = repr(d[1][0])
    r2 = repr(d[1][1])

    if r1 != r2:
        group_count -= 1
    R[r1] = r2
    if group_count == 1:
        print(points[d[1][0]].x*points[d[1][1]].x)
        break


