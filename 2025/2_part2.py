
line = input()
sums = 0


def find(n: int, val_min: int, val_max: int):
    val_str = str(max(pow(10,n-1), val_min))
    result = set()

    part_str = val_str[0:len(val_str) // n]
    while int(part_str * n) <= val_max:
        if int(part_str * n) >= val_min:
            result.add(int(part_str * n))
        part_str = str(int(part_str) + 1)
    return result

for srange in line.split(','):
    val_min, val_max = map(int, srange.split('-'))
    assert val_min <= val_max

    final = set()

    for i in range(2,len(str(val_max))+1):
        final.update(find(i, val_min, val_max))
    sums += sum(final)

print(sums)
