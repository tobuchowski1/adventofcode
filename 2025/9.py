import sys

points = []
for line in sys.stdin:
    line = line.strip()
    points.append(tuple(map(int, line.split(','))))

max_area = 0
for i, p1 in enumerate(points):
    for j,p2 in enumerate(points[i+1:]):
        max_area = max(max_area, (abs(p1[0]-p2[0])+1)*(abs(p1[1]-p2[1])+1)  )

print(max_area)
