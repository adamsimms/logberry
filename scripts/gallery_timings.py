import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config.gallery_hours import GALLERY_HOURS


def are_we_open_yet():
    current_weekday = datetime.now().weekday()
    current_time = datetime.now().strftime("%H:%M")
    hours = GALLERY_HOURS.get(current_weekday)
    if not hours:
        return False
    return hours["open"] <= current_time <= hours["close"]


def next_opening_day():
    open_days = sorted(GALLERY_HOURS.keys())
    current_weekday = datetime.now().weekday()
    for day in open_days:
        if max(open_days) > current_weekday:
            if day > current_weekday:
                return GALLERY_HOURS[day]
        else:
            return GALLERY_HOURS[min(open_days)]
    return GALLERY_HOURS[min(open_days)]


def next_opening_time():
    current_weekday = datetime.now().weekday()
    current_time = datetime.now().strftime("%H:%M")
    open_days = sorted(GALLERY_HOURS.keys())

    if current_weekday in GALLERY_HOURS:
        today = GALLERY_HOURS[current_weekday]
        next_day = GALLERY_HOURS[
            (current_weekday + 1) if current_weekday != max(open_days) else min(open_days)
        ]
        if current_time < today["open"]:
            return "{}, {}".format(today["label"], today["open"])
        if current_time > today["close"]:
            return "{}, {}".format(next_day["label"], next_day["open"])

    return "{}, {}".format(next_opening_day()["label"], next_opening_day()["open"])


def show_offline_message():
    current_time = datetime.now().strftime("%A, %H:%M")
    return "Gallery is closed now at {}. Next show at {}".format(
        current_time, next_opening_time()
    )
