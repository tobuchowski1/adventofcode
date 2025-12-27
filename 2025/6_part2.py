import sys

result = 0
data = []

for line in sys.stdin:
    data.append(line)

chars = [l for l in data[-1].split(" ") if l != ""]

num_list = []
char_num = 0

for c in range(len(data[0]) + 1):
    number = "".join([(line + ' ')[c] for line in data[:-1]]).strip()
    if number == "":
        if chars[char_num] == '+':
            result += sum(num_list)
        elif chars[char_num] == '*':
            partial = 1
            for x in num_list:
                partial *= x
            result += partial
        char_num += 1
        num_list = []
    else:
        num_list.append(int(number))


print(result)
