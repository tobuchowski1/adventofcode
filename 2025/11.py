import sys

result = 0

connection = {}
incoming = {}
paths = {}

for line in sys.stdin:
    line = line.strip()
    name, edges = line.split(':')
    parsed_edges = [e for e in edges.split(" ") if e != ""]
    connection[name] = parsed_edges
    paths[name] = 0 if name != 'you' else 1
    for edge in parsed_edges:
        paths[edge] = 0 if edge != 'you' else 1
        if edge not in incoming:
            incoming[edge] = 1
        else:
            incoming[edge] += 1

leafs = set(connection.keys()) - set(incoming.keys())
total = len(paths)
removed = len(leafs)

while len(leafs) > 0:
    l = leafs.pop()
    if l in connection:
        for e in connection[l]:
            paths[e] += paths[l]
            incoming[e] -= 1
            if incoming[e] == 0:
                leafs.add(e)
                removed += 1

if removed < total:
    print("FOUND CYCLE")

print(paths['out'])