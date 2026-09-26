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


# -------------------------------------------------
# ТЕКУЩАЯ ДАТА И ВРЕМЯ
# -------------------------------------------------

now = datetime.datetime.now()

today = now.date()
current_time = now.time()

day = days[today.weekday()]


# -------------------------------------------------
# ОПРЕДЕЛЯЕМ НЕДЕЛЮ
# -------------------------------------------------

weeks_passed = (today - START_DATE).days // 7

if weeks_passed % 2 == 0:
    week = "НЕЧЁТНАЯ НЕДЕЛЯ"
else:
    week = "ЧЁТНАЯ НЕДЕЛЯ"


# -------------------------------------------------
# ЗАГРУЖАЕМ ASCII-ART
# -------------------------------------------------

with open("girl.txt", "r", encoding="utf-8") as file:
    ascii_girl = file.read()

girl_lines = ascii_girl.splitlines()


# -------------------------------------------------
# ЗАГРУЖАЕМ ВРЕМЯ ПАР
# -------------------------------------------------

pair_times = {}

with open("time.txt", "r", encoding="utf-8") as file:

    for line in file:

        line = line.strip()

        if line == "":
            continue

        number, start, end = line.split(";")

        pair_times[int(number)] = (
            datetime.time.fromisoformat(start),
            datetime.time.fromisoformat(end)
        )


# -------------------------------------------------
# ЗАГРУЖАЕМ РАСПИСАНИЕ
# -------------------------------------------------

with open("schedule.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()


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

    # Получаем пары
    if show_day:

        if line == "":
            break

        schedule.append(line)


# -------------------------------------------------
# ОПРЕДЕЛЯЕМ НОМЕР ПАРЫ
# -------------------------------------------------

current_pair = None
next_pair = None

for pair_number, times in pair_times.items():

    start = times[0]
    end = times[1]

    # Пара сейчас
    if start <= current_time <= end:
        current_pair = pair_number

    # Следующая пара
    elif current_time < start and next_pair is None:
        next_pair = pair_number


# -------------------------------------------------
# ОПРЕДЕЛЯЕМ ТЕКСТ СПРАВА
# -------------------------------------------------

info = []

info.append(f"Сегодня: {today}")
info.append(f"Сейчас: {current_time.strftime('%H:%M')}")
info.append(f"День: {day}")
info.append(f"Неделя: {week}")
info.append("")


# -------------------------------------------------
# ТЕКУЩАЯ / СЛЕДУЮЩАЯ ПАРА
# -------------------------------------------------

if current_pair is not None:

    start, end = pair_times[current_pair]

    info.append(
        f"СЕЙЧАС ИДЁТ {current_pair}-Я ПАРА"
    )

    info.append(
        f"Время: {start.strftime('%H:%M')} - "
        f"{end.strftime('%H:%M')}"
    )

    # Пытаемся найти название этой пары
    index = current_pair - 1

    if index < len(schedule):
        info.append(schedule[index])

elif next_pair is not None:

    start, end = pair_times[next_pair]

    info.append(
        f"СЛЕДУЮЩАЯ ПАРА: {next_pair}-Я"
    )

    info.append(
        f"Время: {start.strftime('%H:%M')} - "
        f"{end.strftime('%H:%M')}"
    )

    index = next_pair - 1

    if index < len(schedule):
        info.append(schedule[index])

else:

    info.append("ПАРЫ НА СЕГОДНЯ ЗАКОНЧИЛИСЬ")


# -------------------------------------------------
# ВСЕ ПАРЫ
# -------------------------------------------------

info.append("")
info.append("РАСПИСАНИЕ НА СЕГОДНЯ")
info.append("-" * 50)


for i, lesson in enumerate(schedule):

    pair_number = i + 1

    if pair_number in pair_times:

        start, end = pair_times[pair_number]

        time_text = (
            f"{start.strftime('%H:%M')}-"
            f"{end.strftime('%H:%M')}"
        )

        info.append(
            f"{pair_number}. [{time_text}] {lesson}"
        )

    else:

        info.append(
            f"{pair_number}. {lesson}"
        )


# -------------------------------------------------
# КОНСОЛЬНЫЙ ИНТЕРФЕЙС
# -------------------------------------------------

print()

print("=" * 110)

print(
    " " * 40 +
    "МОЁ РАСПИСАНИЕ"
)

print("=" * 110)

print()

print(
    f"{'ASCII ART':^45} | {'ИНФОРМАЦИЯ':^60}"
)

print(
    "-" * 45 +
    "-+-" +
    "-" * 60
)


# Максимальное количество строк
max_lines = max(
    len(girl_lines),
    len(info)
)


for i in range(max_lines):

    # Левая часть
    if i < len(girl_lines):
        left = girl_lines[i]
    else:
        left = ""

    # Правая часть
    if i < len(info):
        right = info[i]
    else:
        right = ""

    left = left[:45]

    right = right[:60]

    print(
        f"{left:<45} | {right}"
    )


print()

print("=" * 110)