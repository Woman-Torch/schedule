#ввод данных
print ("Введите день недели")
day = (input()).lower()


with open("schedule.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

show = False

for line in lines:
    line = line.strip()

    if line == day:
        print("\n" + line)
        show = True
        continue

    if show:
        if line == "":
            break

        print(line)