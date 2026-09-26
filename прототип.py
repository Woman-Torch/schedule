import datetime
import tkinter as tk
from tkinter import font


# ==========================================
# НАСТРОЙКИ
# ==========================================

START_DATE = datetime.date(2026, 9, 1)

SCHEDULE_FILE = "schedule.txt"
TIME_FILE = "time.txt"
GIRL_FILE = "girl.txt"

# Цвета терминала
BG = "#000000"
GREEN = "#00ff41"
DARK_GREEN = "#003b16"
BRIGHT_GREEN = "#39ff14"


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
# ASCII-ART
# ==========================================

with open(GIRL_FILE, "r", encoding="utf-8") as file:
    ascii_girl = file.read()


# ==========================================
# ВРЕМЯ ПАР
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
# ПОЛУЧЕНИЕ РАСПИСАНИЯ
# ==========================================

def get_schedule():

    today = datetime.date.today()

    day = days[today.weekday()]

    weeks_passed = (today - START_DATE).days // 7

    if weeks_passed % 2 == 0:
        week = "НЕЧЁТНАЯ НЕДЕЛЯ"
    else:
        week = "ЧЁТНАЯ НЕДЕЛЯ"

    with open(
        SCHEDULE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

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

        if show_day:

            if line == "":
                break

            number, subject = line.split(";", 1)

            schedule.append({
                "number": int(number),
                "subject": subject
            })

    return today, day, week, schedule


# ==========================================
# ОКНО
# ==========================================

root = tk.Tk()

root.title("TERMINAL // SCHEDULE")

root.configure(
    bg=BG
)


# ==========================================
# ШРИФТЫ
# ==========================================

title_font = font.Font(
    family="Courier New",
    size=20,
    weight="bold"
)

info_font = font.Font(
    family="Courier New",
    size=11
)

pair_font = font.Font(
    family="Courier New",
    size=10
)

pair_number_font = font.Font(
    family="Courier New",
    size=12,
    weight="bold"
)


# ==========================================
# ЗАГОЛОВОК
# ==========================================

title = tk.Label(
    root,
    text="[ SYSTEM // SCHEDULE ]",
    bg=BG,
    fg=GREEN,
    font=title_font
)

title.pack(
    pady=(15, 10)
)


# Линия
line = tk.Label(
    root,
    text="=" * 100,
    bg=BG,
    fg=DARK_GREEN,
    font=("Courier New", 9)
)

line.pack()


# ==========================================
# ОСНОВНАЯ ОБЛАСТЬ
# ==========================================

main_frame = tk.Frame(
    root,
    bg=BG
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=15
)


# ==========================================
# ASCII СЛЕВА
# ==========================================

left_frame = tk.Frame(
    main_frame,
    bg=BG,
    padx=20
)

left_frame.pack(
    side="left",
    anchor="n"
)


ascii_label = tk.Label(
    left_frame,
    text=ascii_girl,
    bg=BG,
    fg=GREEN,
    font=("Courier New", 10),
    justify="left",
    anchor="n"
)

ascii_label.pack()


# ==========================================
# ПРАВАЯ ЧАСТЬ
# ==========================================

right_frame = tk.Frame(
    main_frame,
    bg=BG,
    padx=20
)

right_frame.pack(
    side="left",
    fill="both",
    expand=True,
    anchor="n"
)


# ==========================================
# ИНФОРМАЦИЯ
# ==========================================

date_label = tk.Label(
    right_frame,
    bg=BG,
    fg=GREEN,
    font=info_font,
    anchor="w"
)

date_label.pack(
    anchor="w"
)


time_label = tk.Label(
    right_frame,
    bg=BG,
    fg=BRIGHT_GREEN,
    font=("Courier New", 14, "bold"),
    anchor="w"
)

time_label.pack(
    anchor="w"
)


day_label = tk.Label(
    right_frame,
    bg=BG,
    fg=GREEN,
    font=info_font,
    anchor="w"
)

day_label.pack(
    anchor="w"
)


week_label = tk.Label(
    right_frame,
    bg=BG,
    fg=GREEN,
    font=info_font,
    anchor="w"
)

week_label.pack(
    anchor="w",
    pady=(0, 10)
)


# ==========================================
# ТЕКУЩАЯ / СЛЕДУЮЩАЯ ПАРА
# ==========================================

current_frame = tk.Frame(
    right_frame,
    bg=BG,
    highlightbackground=GREEN,
    highlightcolor=GREEN,
    highlightthickness=1,
    padx=15,
    pady=12
)

current_frame.pack(
    fill="x",
    pady=(0, 15)
)


current_title = tk.Label(
    current_frame,
    bg=BG,
    fg=BRIGHT_GREEN,
    font=("Courier New", 13, "bold"),
    anchor="w",
    justify="left"
)

current_title.pack(
    anchor="w"
)


current_info = tk.Label(
    current_frame,
    bg=BG,
    fg=GREEN,
    font=info_font,
    anchor="w",
    justify="left",
    wraplength=650
)

current_info.pack(
    anchor="w",
    pady=(5, 0)
)


# ==========================================
# ЗАГОЛОВОК РАСПИСАНИЯ
# ==========================================

schedule_title = tk.Label(
    right_frame,
    text="[ TODAY'S SCHEDULE ]",
    bg=BG,
    fg=BRIGHT_GREEN,
    font=("Courier New", 13, "bold"),
    anchor="w"
)

schedule_title.pack(
    anchor="w",
    pady=(0, 8)
)


# ==========================================
# СПИСОК ПАР
# ==========================================

schedule_frame = tk.Frame(
    right_frame,
    bg=BG
)

schedule_frame.pack(
    fill="both",
    expand=True
)


# ==========================================
# ОБНОВЛЕНИЕ
# ==========================================

def update_schedule():

    today, day, week, schedule = get_schedule()

    now = datetime.datetime.now()

    current_time = now.time()


    # --------------------------------------
    # Информация
    # --------------------------------------

    date_label.config(
        text=f"[ DATE ]     {today.strftime('%d.%m.%Y')}"
    )

    time_label.config(
        text=f"[ TIME ]     {now.strftime('%H:%M:%S')}"
    )

    day_label.config(
        text=f"[ DAY ]      {day}"
    )

    week_label.config(
        text=f"[ WEEK ]     {week}"
    )


    # --------------------------------------
    # Текущая / следующая пара
    # --------------------------------------

    current_pair = None
    next_pair = None

    for lesson in schedule:

        number = lesson["number"]

        if number not in pair_times:
            continue

        start, end = pair_times[number]


        if start <= current_time <= end:

            current_pair = lesson

        elif current_time < start:

            if next_pair is None:
                next_pair = lesson


    # --------------------------------------
    # Информация о паре
    # --------------------------------------

    if current_pair is not None:

        number = current_pair["number"]

        start, end = pair_times[number]

        current_title.config(
            text=f">>> CURRENT CLASS // #{number}"
        )

        current_info.config(
            text=(
                f"{start.strftime('%H:%M')} - "
                f"{end.strftime('%H:%M')}\n"
                f"{current_pair['subject']}"
            )
        )

    elif next_pair is not None:

        number = next_pair["number"]

        start, end = pair_times[number]

        current_title.config(
            text=f">>> NEXT CLASS // #{number}"
        )

        current_info.config(
            text=(
                f"{start.strftime('%H:%M')} - "
                f"{end.strftime('%H:%M')}\n"
                f"{next_pair['subject']}"
            )
        )

    else:

        current_title.config(
            text=">>> NO MORE CLASSES"
        )

        current_info.config(
            text="Schedule completed for today."
        )


    # --------------------------------------
    # Удаляем старые карточки
    # --------------------------------------

    for widget in schedule_frame.winfo_children():
        widget.destroy()


    # --------------------------------------
    # Создаём карточки
    # --------------------------------------

    for lesson in schedule:

        number = lesson["number"]

        subject = lesson["subject"]


        if number in pair_times:

            start, end = pair_times[number]

            time_text = (
                f"{start.strftime('%H:%M')} - "
                f"{end.strftime('%H:%M')}"
            )

        else:

            time_text = "??:?? - ??:??"


        # Карточка
        card = tk.Frame(
            schedule_frame,
            bg=BG,
            highlightbackground=DARK_GREEN,
            highlightcolor=DARK_GREEN,
            highlightthickness=1,
            padx=8,
            pady=7
        )

        card.pack(
            fill="x",
            pady=3
        )


        # Номер
        number_label = tk.Label(
            card,
            text=f"[{number}]",
            bg=BG,
            fg=BRIGHT_GREEN,
            font=pair_number_font,
            width=5,
            anchor="w"
        )

        number_label.pack(
            side="left",
            anchor="n"
        )


        # Время
        time_label_card = tk.Label(
            card,
            text=time_text,
            bg=BG,
            fg=GREEN,
            font=pair_font,
            width=15,
            anchor="w"
        )

        time_label_card.pack(
            side="left",
            anchor="n"
        )


        # Предмет
        subject_label = tk.Label(
            card,
            text=subject,
            bg=BG,
            fg=GREEN,
            font=pair_font,
            justify="left",
            anchor="w",
            wraplength=650
        )

        subject_label.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10
        )


        # ----------------------------------
        # Текущая пара
        # ----------------------------------

        if current_pair is not None:

            if number == current_pair["number"]:

                card.config(
                    highlightbackground=BRIGHT_GREEN,
                    highlightcolor=BRIGHT_GREEN,
                    highlightthickness=2
                )

                number_label.config(
                    fg=BRIGHT_GREEN
                )


    # --------------------------------------
    # Автоматический размер окна
    # --------------------------------------

    root.update_idletasks()

    width = root.winfo_reqwidth()
    height = root.winfo_reqheight()

    width = max(width, 900)
    height = max(height, 550)

    root.geometry(
        f"{width}x{height}"
    )


    # --------------------------------------
    # Повтор через 1 секунду
    # --------------------------------------

    root.after(
        1000,
        update_schedule
    )


# ==========================================
# ЗАПУСК
# ==========================================

update_schedule()

root.mainloop()