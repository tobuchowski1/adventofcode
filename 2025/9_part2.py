import sys

points = []
for line in sys.stdin:
    line = line.strip()
    points.append(tuple(map(int, line.split(',')[::-1])))

max_area = 0
for i, p1 in enumerate(points):
    for j,p2 in enumerate(points[i+1:]):
        #check if there is a point inside
        should_skip = False
        for z in points:
            if min(p1[0],p2[0]) < z[0] < max(p1[0],p2[0]) and min(p1[1],p2[1]) < z[1] < max(p1[1],p2[1]):
                should_skip = True
                break

        if should_skip:
            continue

        middle = (max(p1[0], p2[0]), (p1[1] + p2[1]) // 2)
        count_crossed = 0
        #check if triangle middle point is inside the structure
        for i, z in enumerate(points):
            y = points[(i+1) % len(points)]
            if z[0] == y[0] and z[0] < middle[0] and min(z[1],y[1]) <= middle[1] <= max([z[1], y[1]]):
                count_crossed += 1

            if z[0] == y[0] and min(z[1],y[1]) <= middle[1] <= max([z[1], y[1]]) and min(p1[0],p2[0]) < z[0] < max([p1[0],p2[0]]):
                should_skip = True
                break

        if should_skip or count_crossed % 2 == 0:
            continue

        area = (abs(p1[0]-p2[0])+1)*(abs(p1[1]-p2[1])+1)
        max_area = max(max_area,  area)

print(max_area)
