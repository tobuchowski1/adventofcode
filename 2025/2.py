
line = input()
sums = 0

for srange in line.split(','):
    val_min, val_max = map(int, srange.split('-'))
    print(val_min, val_max)
    assert val_min <= val_max

    val_str = str(max(10, val_min))
    half_str = val_str[0:len(val_str) // 2]

    while int(half_str + half_str) <= val_max:
        if int(half_str + half_str) >= val_min:
            sums += int(half_str + half_str)
        half_str = str(int(half_str)+1)

    for val in range(val_min, val_max+1):
        val_str = str(val)

print(sums)