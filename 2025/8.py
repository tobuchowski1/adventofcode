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
    for j, p2 in enumerate(points[i+1:],):
        distances.append((distance(p1, p2), (i,i+j+1)))

distances.sort()
R = list(range(len(points)))

def repr(i: int) -> int:
    if R[i] == i:
        return i
    R[i] = repr(R[i])
    return R[i]

for distance in distances[:min(CONNECTIONS_COUNT, len(distances))]:
    R[repr(distance[1][0])] = repr(distance[1][1])

group_sizes = {}
for i in range(len(points)):
    r = repr(i)
    if r in group_sizes:
        group_sizes[r] += 1
    else:
        group_sizes[r] = 1

result = 1
for v in sorted(group_sizes.values(), reverse=True)[:3]:
    result *= v
print(result)
