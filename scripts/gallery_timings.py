from datetime import datetime

timings = {1: ['11:30', '18:30'],
           2: ['11:30', '18:30'],
           3: ['11:30', '18:30'],
           4: ['11:30', '18:30'],
           5: ['11:30', '18:30']}


def are_we_open_yet():
    current_weekday = datetime.weekday(datetime.now())
    current_time = datetime.now().strftime('%H:%m')
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