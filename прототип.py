import datetime
import tkinter as tk


# ==========================================
# НАСТРОЙКИ
# ==========================================

# Дата начала первой НЕЧЁТНОЙ недели
START_DATE = datetime.date(2026, 9, 1)

SCHEDULE_FILE = "schedule.txt"
TIME_FILE = "time.txt"
GIRL_FILE = "girl.txt"


# ==========================================
# ДНИ НЕДЕЛИ
# ==========================================

days = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье"
]


# ==========================================
# ТЕКУЩАЯ ДАТА И ВРЕМЯ
# ==========================================

now = datetime.datetime.now()

today = now.date()
current_time = now.time()

day = days[today.weekday()]


# ==========================================
# ОПРЕДЕЛЯЕМ ЧЁТНОСТЬ НЕДЕЛИ
# ==========================================

weeks_passed = (today - START_DATE).days // 7

if weeks_passed % 2 == 0:
    week = "НЕЧЁТНАЯ НЕДЕЛЯ"
else:
    week = "ЧЁТНАЯ НЕДЕЛЯ"


# ==========================================
# ЗАГРУЖАЕМ ASCII-ART
# ==========================================

with open(GIRL_FILE, "r", encoding="utf-8") as file:
    ascii_girl = file.read()


# ==========================================
# ЗАГРУЖАЕМ ВРЕМЯ ПАР
# ==========================================

pair_times = {}

with open(TIME_FILE, "r", encoding="utf-8") as file:

    for line in file:

        line = line.strip()

        if line == "":
            continue

        number, start, end = line.split(";")

        pair_times[int(number)] = (
            datetime.time.fromisoformat(start),
            datetime.time.fromisoformat(end)
        )


# ==========================================
# ЗАГРУЖАЕМ РАСПИСАНИЕ
# ==========================================

with open(SCHEDULE_FILE, "r", encoding="utf-8") as file:
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

        # Формат:
        # 6;Инклюзивная компетентность
        number, subject = line.split(";", 1)

        schedule.append({
            "number": int(number),
            "subject": subject
        })


# ==========================================
# ИЩЕМ ТЕКУЩУЮ И СЛЕДУЮЩУЮ ПАРУ
# ==========================================

current_pair = None
next_pair = None

for lesson in schedule:

    pair_number = lesson["number"]

    if pair_number not in pair_times:
        continue

    start, end = pair_times[pair_number]

    # Сейчас идёт эта пара
    if start <= current_time <= end:
        current_pair = lesson

    # Это ближайшая будущая пара
    elif current_time < start and next_pair is None:
        next_pair = lesson


# ==========================================
# СОЗДАЁМ ОКНО
# ==========================================

root = tk.Tk()

root.title("Моё расписание")

root.geometry("1100x750")

root.minsize(900, 600)


# ==========================================
# ЗАГОЛОВОК
# ==========================================

title = tk.Label(
    root,
    text="МОЁ РАСПИСАНИЕ",
    font=("Arial", 24, "bold")
)

title.pack(pady=10)


# ==========================================
# ОСНОВНОЙ КОНТЕЙНЕР
# ==========================================

main_frame = tk.Frame(root)

main_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)


# ==========================================
# ЛЕВАЯ ЧАСТЬ — ASCII
# ==========================================

left_frame = tk.Frame(
    main_frame,
    width=450
)

left_frame.pack(
    side="left",
    fill="both",
    expand=False,
    padx=10
)

ascii_label = tk.Label(
    left_frame,
    text=ascii_girl,
    font=("Courier New", 10),
    justify="left",
    anchor="n"
)

ascii_label.pack(
    fill="both",
    expand=True
)


# ==========================================
# ПРАВАЯ ЧАСТЬ
# ==========================================

right_frame = tk.Frame(main_frame)

right_frame.pack(
    side="right",
    fill="both",
    expand=True,
    padx= 150
)


# ==========================================
# ИНФОРМАЦИЯ О СЕГОДНЯ
# ==========================================

date_label = tk.Label(
    right_frame,
    text=f"Сегодня: {today.strftime('%d.%m.%Y')}",
    font=("Arial", 14)
)

date_label.pack(anchor="w")


time_label = tk.Label(
    right_frame,
    text=f"Сейчас: {current_time.strftime('%H:%M:%S')}",
    font=("Arial", 14)
)

time_label.pack(anchor="w")


day_label = tk.Label(
    right_frame,
    text=f"День: {day}",
    font=("Arial", 14)
)

day_label.pack(anchor="w")


week_label = tk.Label(
    right_frame,
    text=f"Неделя: {week}",
    font=("Arial", 14, "bold")
)

week_label.pack(anchor="w", pady=(0, 10))


# ==========================================
# ТЕКУЩАЯ / СЛЕДУЮЩАЯ ПАРА
# ==========================================

if current_pair is not None:

    number = current_pair["number"]

    start, end = pair_times[number]

    current_text = (
        f"СЕЙЧАС ИДЁТ {number}-Я ПАРА\n\n"
        f"{start.strftime('%H:%M')} - "
        f"{end.strftime('%H:%M')}\n\n"
        f"{current_pair['subject']}"
    )

elif next_pair is not None:

    number = next_pair["number"]

    start, end = pair_times[number]

    current_text = (
        f"СЛЕДУЮЩАЯ ПАРА — {number}-Я\n\n"
        f"{start.strftime('%H:%M')} - "
        f"{end.strftime('%H:%M')}\n\n"
        f"{next_pair['subject']}"
    )

else:

    current_text = "ПАР НА СЕГОДНЯ БОЛЬШЕ НЕТ"


current_label = tk.Label(
    right_frame,
    text=current_text,
    font=("Arial", 14, "bold"),
    justify="left",
    anchor="w",
    relief="groove",
    padx=15,
    pady=15
)

current_label.pack(
    fill="x",
    pady=10
)


# ==========================================
# ЗАГОЛОВОК РАСПИСАНИЯ
# ==========================================

schedule_title = tk.Label(
    right_frame,
    text="РАСПИСАНИЕ НА СЕГОДНЯ",
    font=("Arial", 16, "bold")
)

schedule_title.pack(
    anchor="w",
    pady=5
)


# ==========================================
# СПИСОК ПАР
# ==========================================

schedule_frame = tk.Frame(right_frame)

schedule_frame.pack(
    fill="both",
    expand=True
)


scrollbar = tk.Scrollbar(
    schedule_frame
)

scrollbar.pack(
    side="right",
    fill="y"
)


schedule_text = tk.Text(
    schedule_frame,
    font=("Arial", 11),
    yscrollcommand=scrollbar.set,
    wrap="word"
)

schedule_text.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.config(
    command=schedule_text.yview
)


# ==========================================
# ВЫВОДИМ ВСЕ ПАРЫ
# ==========================================

if len(schedule) == 0:

    schedule_text.insert(
        "end",
        "Сегодня пар нет."
    )

else:

    for lesson in schedule:

        number = lesson["number"]
        subject = lesson["subject"]

        if number in pair_times:

            start, end = pair_times[number]

            time_text = (
                f"{start.strftime('%H:%M')} - "
                f"{end.strftime('%H:%M')}"
            )

            schedule_text.insert(
                "end",
                f"{number}.  [{time_text}]\n"
            )

            schedule_text.insert(
                "end",
                f"    {subject}\n\n"
            )

        else:

            schedule_text.insert(
                "end",
                f"{number}. {subject}\n\n"
            )


schedule_text.config(
    state="disabled"
)


# ==========================================
# ОБНОВЛЕНИЕ ВРЕМЕНИ
# ==========================================

def update_clock():

    current = datetime.datetime.now()

    time_label.config(
        text=f"Сейчас: {current.strftime('%H:%M:%S')}"
    )

    root.after(
        1000,
        update_clock
    )


update_clock()


# ==========================================
# ЗАПУСК
# ==========================================

root.mainloop()