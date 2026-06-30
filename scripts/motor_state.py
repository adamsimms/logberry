from config import data_input

lowest_tide = data_input.lowest_tide
tide_range = data_input.tide_range
multiplier = data_input.multiplier
speed_multiplier = data_input.speed_multiplier
speed_steps_per_minute = round(40 * speed_multiplier)

Motor0 = None
Motor1 = None

tide_data = None
previous_from_position = 0
previous_to_position = 0
current_from_position = 0
current_to_position = 0
tide_distance_count = 0
time_of_new_tide_data = 0
global_wave_timing = []


def init_motors():
    global Motor0, Motor1
    import Slush

    Slush.sBoard()
    Motor0 = Slush.Motor(0)
    Motor1 = Slush.Motor(3)
