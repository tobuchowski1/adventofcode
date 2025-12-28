import sys
from queue import Queue

result = 0

max_reps = 0
max_len = 0
max_buttons = 0

ll = ["[#....#...] (3,5,6,8) (1,6) (1,2,4,7,8) (3,4,5,7,8) (0,2,4,5,6,8) (0,1,3) (1,2,6,7,8) (0,5) (0,1,4,6,8) {42,46,38,34,52,33,33,36,61}"]
l2 = ["[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"]
l5 = ["[##..] (1,3) (1) (1,2) (0,1) (2,3) {13,66,31,27}"]
l6 = ["[##..#] (1,2,4) (1,2) (1,3,4) (1,2,3) (2,3) (0,2,3) (2,4) {13,49,69,58,49}"]
l7 = ["[#.##...#..] (0,4,5,8) (2,3,6,7,8,9) (0,1,6) (3,4,7) (0,9) (0,2,3,4,7,8,9) (2,3,8) (1,4,9) (0,1,2,3,4,5,9) (1,2,4,6,7,8) (0,1,2,4,5,6) (0,1,4,5,6,9) {72,52,56,61,88,33,32,44,56,47}"]

l8 = ["[.##..] (1,2) (0,2,3,4) (0,1,3,4) {17,20,19,17,17}"]
l9 = ["[##....#...] (2,3,4,5,6,7) (0,1,2,3,4,6,9) (0,1,3,4,6,8,9) (1,2,3,4,6) (1,4,5,6,8,9) (2,4,5,8,9) (0,1,3,4,5,8,9) (0,1,2,6) (2,7,8,9) (1,2,4,8) (3,4,6,7,8,9) (0,2,5,7,8) (0,1,2,4,5,6,8,9) {79,95,119,80,137,88,128,63,122,126}"]
# 164?

for line in l9:
    line = line.strip()
    data = line.split(" ")
    # print(line)
    start_pos = 0
    target = []
    buttons: dict[int, list[list[int]]] = {}
    indicator_count = 0
    for d in data:
        if d.startswith("["):
            indicator_count = len(d.removesuffix(']').removeprefix('['))
            max_len=max(max_len,indicator_count)
        if d.startswith("{"):
            for c in d.removesuffix('}').removeprefix('{').split(","):
                target.append(int(c))
                max_reps=max(max_reps, int(c))
        elif d.startswith("("):
            button = [0] * indicator_count
            for n in d.removeprefix('(').removesuffix(')').split(','):
                button[int(n)] = 1
            idx = min([i for i, v in enumerate(button) if v != 0])
            if idx not in buttons:
                buttons[idx] = []
            buttons[idx].append(button)
    max_buttons = max(max_buttons, sum([len(v) for v in buttons.values()]))
    q = Queue()
    visited = set()
    step = 0

    # if indicator_count > 7:
    #     continue

    q.put((0, [0] * indicator_count, 0, 0))
    while not q.empty():
        step += 1
        depth, pos,  b_idx, t_idx = q.get()
        # print(depth, pos, ">>", target, step)
        if pos == target:
            print(line + f" ?{depth}?")
            result += depth
            break

        if pos[t_idx] < target[t_idx]: # and i in buttons:
            for nb_idx, b in enumerate(buttons[t_idx][b_idx:]):
                new_pos = [x + y for x, y in zip(pos, b)]
                if str(new_pos) in visited:
                    continue
                # if b[t_idx] + pos[t_idx] <= target[t_idx]:
                if all([x >= y for x, y in zip(target, new_pos)]):
                    # if depth == 10:
                    #     breakpoint()
                    visited.add(str(new_pos))
                    q.put((depth+1, new_pos, nb_idx, t_idx))
        elif pos[t_idx] == target[t_idx]:
            idx = t_idx
            while pos[idx] == target[idx]:
                idx += 1
            if idx in buttons:
                for nb_idx, b in enumerate(buttons[idx]):
                    new_pos = [x + y for x, y in zip(pos, b)]
                    if str(new_pos) not in visited:
                        visited.add(str(new_pos))
                        q.put((depth + 1, new_pos, nb_idx, idx))

# print(max_len, max_reps, max_buttons)
print(result)

