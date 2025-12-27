import sys

result = 0

connection = {}
incoming = {}
paths = {}

def calculate_paths(start: str, end: str) -> int:
    paths_tmp = paths.copy()
    leafs = set(connection.keys()) - set(incoming.keys())
    total = len(paths)
    removed = len(leafs)
    incoming_tmp = incoming.copy()
    paths_tmp[start] = 1

    while len(leafs) > 0:
        l = leafs.pop()
        if l in connection:
            for e in connection[l]:
                paths_tmp[e] += paths_tmp[l]
                incoming_tmp[e] -= 1
                if incoming_tmp[e] == 0:
                    leafs.add(e)
                    removed += 1

    if removed < total:
        print("FOUND CYCLE")

    return paths_tmp[end]

for line in sys.stdin:
    line = line.strip()
    name, edges = line.split(':')
    parsed_edges = [e for e in edges.split(" ") if e != ""]
    connection[name] = parsed_edges
    paths[name] = 0
    for edge in parsed_edges:
        paths[edge] = 0
        if edge not in incoming:
            incoming[edge] = 1
        else:
            incoming[edge] += 1

option1 = calculate_paths('svr', 'fft')*calculate_paths('fft', 'dac')*calculate_paths('dac', 'out')
option2 = calculate_paths('svr', 'dac')*calculate_paths('dac', 'fft')*calculate_paths('fft', 'out')
print(option1+option2)
