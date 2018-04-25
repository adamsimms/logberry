from datetime import datetime

timings = {1: ['11:30', '18:30', "Tuesday"],
           2: ['11:30', '18:30', "Wednesday"],
           3: ['11:30', '18:30', "Thursday"],
           4: ['11:30', '18:30', "Friday"],
           5: ['11:30', '18:30', "Saturday"]}


def are_we_open_yet():
    current_weekday = datetime.weekday(datetime.now())
    current_time = datetime.now().strftime('%H:%M')
    if current_weekday in timings.keys():
        opening_times = timings[current_weekday]
        start_at = opening_times[0]
        end_at = opening_times[1]
        if (current_time >= start_at) and (current_time <= end_at):
            return True
        else:
            return False
    else:
        return False

def next_opening_day(timings=timings):
    open_days = list(timings.keys())
    open_days.sort()
    current_weekday = datetime.weekday(datetime.now())
    for day in open_days:
        if max(open_days) > current_weekday:
            if day > current_weekday:
                return timings[day]
            else:
                continue
        else:
            return timings[min(open_days)]

def next_opening_time():
    current_weekday = datetime.weekday(datetime.now())
    current_time = datetime.now().strftime('%H:%M')
    days_open = timings.keys()
    if current_weekday in days_open:
        opening_times_today = timings[current_weekday]
        opening_times_next = timings[(current_weekday+1) if current_weekday != max(days_open) else min(days_open)]
        if current_time < opening_times_today[0]:
            return "{}, {}".format(opening_times_today[2], opening_times_today[0])
        elif current_time > opening_times_today[1]:
            return "{}, {}".format(opening_times_next[2], opening_times_next[0])
    else:
        opening_times_next = next_opening_day(timings=timings)
        return "{}, {}".format(opening_times_next[2], opening_times_next[0])

def show_offline_message():
    current_time = datetime.now().strftime('%A, %H:%M')
    return "Gallery is closed now at {}. Next show at {}".format(current_time, next_opening_time())
