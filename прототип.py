import datetime

# Дата начала первой НЕЧЁТНОЙ недели
START_DATE = datetime.date(2026, 9, 1)

days = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье"
]

# Текущая дата
today = datetime.date.today()

# День недели
day = days[today.weekday()]

# Сколько недель прошло
weeks_passed = (today - START_DATE).days // 7

# Определяем неделю
if weeks_passed % 2 == 0:
    week = "НЕЧЁТНАЯ НЕДЕЛЯ"
else:
    week = "ЧЁТНАЯ НЕДЕЛЯ"


# Читаем ASCII-девочку
with open("girl.txt", "r", encoding="utf-8") as file:
    ascii_girl = file.read()

girl_lines = ascii_girl.splitlines()


# Читаем расписание
with open("schedule.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()


# Ищем нужную неделю и день
show_week = False
show_day = False
schedule = []

for line in lines:

    line = line.strip()

    # Нашли нужную неделю
    if line == week:
        show_week = True
        continue

    # Началась другая неделя
    if show_week and line in [
        "НЕЧЁТНАЯ НЕДЕЛЯ",
        "ЧЁТНАЯ НЕДЕЛЯ"
    ]:
        break

    # Нашли сегодняшний день
    if show_week and line == day:
        show_day = True
        continue

    # Если нашли расписание
    if show_day:

        # Пустая строка означает конец дня
        if line == "":
            break

        schedule.append(line)


# Заголовок
print()
print("=" * 100)
print(" " * 35 + "МОЁ РАСПИСАНИЕ")
print("=" * 100)
print()


# Заголовки двух частей
print(f"{'ASCII ART':^45} | {'РАСПИСАНИЕ':^50}")
print("-" * 45 + "-+-" + "-" * 50)


# Максимальное количество строк
max_lines = max(len(girl_lines), len(schedule) + 5)


for i in range(max_lines):

    # Левая часть
    if i < len(girl_lines):
        left = girl_lines[i]
    else:
        left = ""

    # Правая часть
    if i == 0:
        right = f"Сегодня: {today}"
    elif i == 1:
        right = f"День: {day}"
    elif i == 2:
        right = f"Неделя: {week}"
    elif i == 3:
        right = ""
    elif i == 4:
        right = "-" * 48
    elif i - 5 < len(schedule):
        right = schedule[i - 5]
    else:
        right = ""

    # Ограничиваем левую часть
    left = left[:45]

    print(f"{left:<45} | {right}")


print()
print("=" * 100)