import sys
from enum import Enum

result = 0
steps = 0

class Failure(Enum):
    NOT_FOUND = 0
    NEGATIVE_VECTOR = 1
    NO_POSSIBLE_VALUE = 2


def gauss(vectors: list[list[int]]) -> list[list[int]]:
    global steps
    steps += 1
    matrix = [v.copy() for v in vectors]

    n = min(len(matrix), len(matrix[0]))
    for i in range(n):
        selected = i
        current_best = len(matrix[i]) + 1
        for j in range(i,len(matrix)):
            non_zero_count = len([m for m in matrix[j][:-1] if m != 0])
            if matrix[j][i] == 1 and non_zero_count < current_best:
                current_best = non_zero_count
                selected = j
            elif matrix[j][i] != 0 and current_best == len(matrix[i]) + 1:
                selected = j

        if selected != i:
            matrix[selected], matrix[i] = matrix[i], matrix[selected]

        if matrix[i][i] not in  (0,1):
            if matrix[i][i] < 0:
                matrix[i] = [-v for v in matrix[i]]
            elif all([v%matrix[i][i] == 0 for v in matrix[i]]):
                matrix[i] = [v // matrix[i][i] for v in matrix[i]]

        for j,v in enumerate(matrix):
            if v[i] != 0 and matrix[i][i] != 0 and j != i:
                times = v[i] // matrix[i][i]
                # print(f"subtracting {i} times {times} from {j}")
                matrix[j] = [x - times * y for x,y in zip(v,matrix[i])]

    # remove rows with all 0s
    matrix = [m for m in matrix if any(x != 0 for x in m)]
    return matrix

def loop_gauss_till_halt(vectors_original: list[list[int]]) -> list[list[int]]:
    vectors = vectors_original
    gaussian = gauss(vectors)
    while vectors != gaussian:
        vectors = gaussian
        gaussian = gauss(vectors)
    return gaussian

def guess_target(input_vectors: list[list[int]]) -> list[list[int]] | Failure:
    starting_sum = max([v[-1] for v in input_vectors])
    max_reps = sum([v[-1] for v in input_vectors])
    gaussian_result = Failure.NOT_FOUND
    while isinstance(gaussian_result, Failure) and starting_sum <= max_reps:
        # print(f"trying {starting_sum}")
        tv = ([1] * (len(input_vectors[0])-1)) + [starting_sum]
        gaussian_result = resolve_variables(input_vectors + [tv], starting_sum)
        starting_sum += 1
    return gaussian_result

def resolve_variables(input_vectors: list[list[int]], max_reps: int) -> list[list[int]] | Failure:
    def bind_var(idx: int, val: int, selected_vector: list[int], vectors_to_bind: list[list[int]]) -> list[list[int]] | Failure:
        # print(f"binding {idx} {selected_vector} to {val}")
        split_first = [0] * len(selected_vector)
        split_first[idx] = 1
        split_first[-1] = val

        split_second = selected_vector.copy()
        split_second[idx] = 0
        split_second[-1] -= val

        new_input = [v.copy() for v in vectors_to_bind] + [split_first, split_second]
        return resolve_variables(new_input, max_reps)

    gaussian = loop_gauss_till_halt(input_vectors)
    # print(f"gaussian {gaussian}")

    if all([sum(v[:-1])==1 for v in gaussian]):
        if any(v[-1]<0 for v in gaussian):
            return Failure.NEGATIVE_VECTOR
        return gaussian

    for v in gaussian:
        if v[-1] < 0 and all(x>=0 for x in v[:-1]):
            return Failure.NEGATIVE_VECTOR
        non_zero_cols = [x for x in v[:-1] if x != 0]
        if len(non_zero_cols) == 1 and v[-1] != 0:
            if v[-1]%non_zero_cols[0] != 0:
                return Failure.NO_POSSIBLE_VALUE

    best_gaussian = Failure.NOT_FOUND
    best_sum = 1000000000

    bindings = []
    for v_idx,v in enumerate(gaussian):
        ones_cols = [i for i,y in enumerate(v[:-1]) if y == 1] # TODO y > 0 should work instead
        non_zero_cols = len([x for x in v[:-1] if x !=0])
        if non_zero_cols == 0 and v[-1] != 0:
            return Failure.NOT_FOUND
        if non_zero_cols > 1 and v[-1] > 0 and ones_cols:
            idx = ones_cols[0]
            max_val = (v[-1] // v[idx]) + 1
            if any([x < 0 for x in v[:-1]]):
                max_val = max_reps + 1
            bindings.append((max_val, idx, v_idx))
        elif non_zero_cols > 1 and v[-1] == 0 and all([x>=0 for x in v[:-1]]):
            idx = [i for i,y in enumerate(v[:-1]) if y != 0][0]
            bindings.append((1, idx, v_idx))
        #     breakpoint()

    if len(bindings) > 0:
        bindings.sort(key=lambda x: x[0])
        max_val, vv_idx, v_idx = bindings[0]
        for val in range(max_val)[::-1]:
            nresult = bind_var(vv_idx, val, gaussian[v_idx], gaussian)
            if not isinstance(nresult, Failure):
                nsum = sum([v[-1] for v in nresult])
                if best_sum > nsum:
                    best_sum = nsum
                    best_gaussian = nresult
                else:
                    # there can only be one local minimum
                    break

    return best_gaussian


lslow = ["[##.##.....] (1,3,7,8) (1,3,5,8) (0,2,3,4,5,6,8) (8) (0,1,2,3,5,7,8,9) (0,2,6,7) (4,6,7) (0,1,7,8,9) (2,3,5,8,9) (0,4,5,6) (1,4,5,9) (2,3,4,6,8,9) (2,4,6,8,9) {220,54,231,228,238,235,238,54,267,70} ?301?"]
lt = ["[..##.#] (0,1,2,5) (0,1,5) (0,5) (2,4) (2,3,5) (0,3,4) {223,218,44,22,9,239}"]

# for line in lslow:
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

    gaussian = guess_target(vectors)

    # print(gaussian)
    # reconstruct
    reconstruction = [sum(v[i] * gaussian[j][-1] for j,v in enumerate(buttons)) for i in range(len(buttons[0]))]
    # print(">>", reconstruction)
    assert reconstruction == target

    partial_result = sum([g[-1] for g in gaussian])
    print(">>result:", partial_result, steps)
    # print(f"with {steps} steps")
    if expected_result is not None:
        assert partial_result == expected_result

    result += partial_result

print(result)
