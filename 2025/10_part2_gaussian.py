import sys

result = 0

# def search(idx: int, vectors: list[list[int]], button_order, bound: dict[int,int], target: list[int]) -> list[int]:

def gauss(vectors: list[list[int]]) -> list[list[int]]:
    matrix = [v.copy() for v in vectors]

    n = min(len(matrix), len(matrix[0]))
    for i in range(n):
        selected = i
        for j in range(i,n):
            if matrix[j][i] == 1:
                selected = j
                break
            elif matrix[j][i] != 0:
                selected = j

        if selected != i:
            matrix[selected], matrix[i] = matrix[i], matrix[selected]

        if matrix[i][i] not in  (0,1):
            if matrix[i][i] < 0:
                matrix[i] = [-v for v in matrix[i]]
            elif all([v%matrix[i][i] == 0 for v in matrix[i]]):
                matrix[i] = [v // matrix[i][i] for v in matrix[i]]

        for j in range(n):
            if matrix[j][i] != 0 and matrix[i][i] != 0 and j != i:
                times = matrix[j][i] // matrix[i][i]
                matrix[j] = [x - times * y for x,y in zip(matrix[j],matrix[i])]

    # remove rows with all 0s
    matrix = [m for m in matrix if any(x != 0 for x in m)]

    return matrix

def loop_gauss_till_halt(vectors_original: list[list[int]]) -> list[list[int]]:
    vectors = vectors_original
    gaussian = gauss(vectors)
    while vectors != gaussian:
        print(vectors, "??", gaussian)
        vectors = gaussian
        gaussian = gauss(vectors)

    return gaussian

def resolve_variables(input_vectors: list[list[int]]) -> list[list[int]] | None:
    gaussian = loop_gauss_till_halt(input_vectors)
    gresult = [sum([v[i] for v in gaussian]) for i in range(len(gaussian[0]))]

    if all([x==1 for x in gresult[:-1]]):
        if any(v[-1]<0 for v in gaussian):
            return None
        return gaussian

    # breakpoint()

    for v in gaussian:
        if sum([x for x in v[:-1]]) > 1:
            idx = [i for i,y in enumerate(v) if y != 0][0]
            for val in range(v[-1]+1)[::-1]:
                split_first = [0] * len(v)
                split_first[idx] = 1
                split_first[-1] = val

                split_second = v.copy()
                split_second[idx] = 0
                split_second[-1] -= val

                new_input = [v.copy() for v in input_vectors] + [split_first,split_second]

                nresult = resolve_variables(new_input)
                if nresult != None:
                    return nresult

    return None


ll = ["[#....#...] (3,5,6,8) (1,6) (1,2,4,7,8) (3,4,5,7,8) (0,2,4,5,6,8) (0,1,3) (1,2,6,7,8) (0,5) (0,1,4,6,8) {42,46,38,34,52,33,33,36,61}"] # 79
l2 = ["[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"] # 10
l3 = ["[..] (0,1) (1) (0) {3,3}"]
l4 = ["[...] (0,2) (0,1) (0,1,2) {8,7,7}"]
l5 = ["[##..] (1,3) (1) (1,2) (0,1) (2,3) {13,66,31,27}"] # 69
l8 = ["[.##..] (1,2) (0,2,3,4) (0,1,3,4) {17,20,19,17,17}"]

for line in l8:
    line = line.strip()
    data = line.split(" ")
    print(line)
    target = []
    buttons: list[list[int]] = []
    button_lengths = []
    indicator_count = 0
    for d in data:
        if d.startswith("["):
            indicator_count = len(d.removesuffix(']').removeprefix('['))
        if d.startswith("{"):
            for c in d.removesuffix('}').removeprefix('{').split(","):
                target.append(int(c))
        elif d.startswith("("):
            button = [0] * indicator_count
            for n in d.removeprefix('(').removesuffix(')').split(','):
                button[int(n)] = 1
            buttons.append(button)

    # sort to prioritize using longest buttons the most times
    buttons.sort(key=lambda bt: sum(bt), reverse=True)

    vectors = []
    for i in range(indicator_count):
        vector = []
        for b in buttons:
            vector.append(b[i])
        vector.append(target[i])
        vectors.append(vector)

    print(vectors)

    gaussian = resolve_variables(vectors)

    print(gaussian)
    print([sum([v[i] for v in gaussian]) for i in range(len(gaussian[0]))])

    # reconstruct
    print(">>", [sum(v[i] * gaussian[j][-1] for j,v in enumerate(buttons)) for i in range(len(buttons[0]))])

    print(sum([g[-1] for g in gaussian]))


