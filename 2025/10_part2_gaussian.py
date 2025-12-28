import sys
from enum import Enum

result = 0
steps = 0

class Failure(Enum):
    NOT_FOUND = 0
    NEGATIVE_VECTOR = 1


def gauss(vectors: list[list[int]]) -> list[list[int]]:
    global steps
    steps += 1
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
        # print(vectors, "??", gaussian)
        vectors = gaussian
        gaussian = gauss(vectors)
    return gaussian

def guess_target(input_vectors: list[list[int]]) -> list[list[int]] | Failure:
    starting_sum = max([v[-1] for v in input_vectors])
    gaussian_result = Failure.NOT_FOUND
    while isinstance(gaussian_result, Failure):
        print(f"trying {starting_sum}")
        tv = ([1] * (len(input_vectors[0])-1)) + [starting_sum]
        gaussian_result = resolve_variables(input_vectors + [tv])
        starting_sum += 1
    return gaussian_result

def resolve_variables(input_vectors: list[list[int]]) -> list[list[int]] | Failure:
    def bind_var(idx: int, val: int, selected_vector: list[int]) -> list[list[int]] | Failure:
        split_first = [0] * len(selected_vector)
        split_first[idx] = 1
        split_first[-1] = val

        split_second = selected_vector.copy()
        split_second[idx] = 0
        split_second[-1] -= val

        new_input = [v.copy() for v in input_vectors] + [split_first, split_second]
        return resolve_variables(new_input)

    gaussian = loop_gauss_till_halt(input_vectors)
    # gresult = [sum([v[i] for v in gaussian]) for i in range(len(gaussian[0]))]
    # print(gaussian)

    if all([sum(v[:-1])==1 for v in gaussian]):
        if any(v[-1]<0 for v in gaussian):
            # breakpoint()
            return Failure.NEGATIVE_VECTOR
        # breakpoint()
        return gaussian

    # breakpoint()
    best_gaussian = Failure.NOT_FOUND
    best_sum = 1000000000
    for v in gaussian[:-1]:
        if sum([x for x in v[:-1]]) > 1 and v[-1] > 0:
            idx = [i for i,y in enumerate(v) if y != 0][0]

            # lo = 0
            # hi = v[-1]
            # value_cache = {}
            #
            # while lo < hi:
            #     mid = (lo + hi) // 2
            #
            #     if mid not in value_cache:
            #         value_cache[mid] = bind_var(idx, mid, v)
            #
            #     if (mid+1) not in value_cache:
            #         value_cache[mid+1] = bind_var(idx, mid + 1, v)
            #
            #     if value_cache[mid + 1] is Failure.NEGATIVE_VECTOR:
            #         hi = mid
            #         continue
            #
            #     if value_cache[mid] is Failure.NOT_FOUND:
            #         lo = mid + 1
            #         continue
            #
            #     if isinstance(value_cache[mid], Failure) or isinstance(value_cache[mid+1], Failure):
            #         breakpoint()
            #
            #     if value_cache[mid] > value_cache[mid + 1]:
            #         lo = mid + 1
            #     else:
            #         hi = mid
            #
            # return value_cache[lo]


            for val in range(v[-1]+1)[::-1]:
                nresult = bind_var(idx, val, v)
                if not isinstance(nresult, Failure):
                    # return nresult
                    nsum = sum([v[-1] for v in nresult])
                    # if idx == 1:
                    #     print(val,nsum)

                    if best_sum > nsum:
                        best_sum = nsum
                        best_gaussian = nresult
                    else:
                        break
                # elif idx == 1:
                #     print(val,nresult)
            break

    # breakpoint()
    return best_gaussian


ll = ["[#....#...] (3,5,6,8) (1,6) (1,2,4,7,8) (3,4,5,7,8) (0,2,4,5,6,8) (0,1,3) (1,2,6,7,8) (0,5) (0,1,4,6,8) {42,46,38,34,52,33,33,36,61}"] # 79
l2 = ["[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"] # 10
l3 = ["[..] (0,1) (1) (0) {3,3}"]
l4 = ["[...] (0,2) (0,1) (0,1,2) {8,7,7}"]
l5 = ["[##..] (1,3) (1) (1,2) (0,1) (2,3) {13,66,31,27}"] # 69
l8 = ["[.##..] (1,2) (0,2,3,4) (0,1,3,4) {17,20,19,17,17} ?28?"]
l9 = ["[##.#] (0) (0,1) (1,2,3) (1,2) (2,3) {184,206,50,38} ?234?"] # 60 steps
l10 = ["[.##.] (0,2) (1) (1,3) (0,3) (2,3) (3) {19,12,14,41} ?43?"] # 1067 steps
l11 = ["[##..#] (1,2,4) (1,2) (1,3,4) (1,2,3) (2,3) (0,2,3) (2,4) {13,49,69,58,49} ?88?"] # 95 958 steps
l12 = ["[##....#...] (2,3,4,5,6,7) (0,1,2,3,4,6,9) (0,1,3,4,6,8,9) (1,2,3,4,6) (1,4,5,6,8,9) (2,4,5,8,9) (0,1,3,4,5,8,9) (0,1,2,6) (2,7,8,9) (1,2,4,8) (3,4,6,7,8,9) (0,2,5,7,8) (0,1,2,4,5,6,8,9) {79,95,119,80,137,88,128,63,122,126}"]

for line in sys.stdin:
    line = line.strip()
    data = line.split(" ")
    print(line)
    target = []
    buttons: list[list[int]] = []
    button_lengths = []
    indicator_count = 0
    expected_result = None
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
        elif d.startswith("?"):
            expected_result = int(d.replace("?",""))

    # sort to prioritize using longest buttons the most times
    buttons.sort(key=lambda bt: sum(bt), reverse=True)

    vectors = []
    for i in range(indicator_count):
        vector = []
        for b in buttons:
            vector.append(b[i])
        vector.append(target[i])
        vectors.append(vector)

    # print(vectors)

    gaussian = guess_target(vectors)

    # print("b", buttons)
    # print(gaussian)
    # print([sum([v[i] for v in gaussian]) for i in range(len(gaussian[0]))])

    # reconstruct
    # print(">>", [sum(v[i] * gaussian[j][-1] for j,v in enumerate(buttons)) for i in range(len(buttons[0]))])

    partial_result = sum([g[-1] for g in gaussian])
    print(">>result:", partial_result, steps)
    # print(f"with {steps} steps")
    if expected_result is not None:
        assert partial_result == expected_result

    result += partial_result

print(result)
