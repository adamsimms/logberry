import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import gallery_timings
import motor_state as state
import tide_data as tide
import wave_data as wave
from motor_session import closing_action, starting_act, tide_data_refresh
from motor_utils import motor_reset, wait_for_motors

tide.get_tide_data()
wave.get_wave_data()

state.init_motors()
motor_reset(state.Motor0)
motor_reset(state.Motor1)

is_motor_on = 0

while True:
    try:
        if gallery_timings.are_we_open_yet():
            if is_motor_on == 0:
                starting_act()
            print("gallery is open")
            tide_data_refresh()
            is_motor_on = 1
            continue

        if is_motor_on == 1:
            print("gallery is closing now")
            closing_action()
            is_motor_on = 0
            continue

        state.Motor0.setCurrent(hold=0, run=0, acc=0, dec=0)
        state.Motor1.setCurrent(hold=0, run=0, acc=0, dec=0)
        print(gallery_timings.show_offline_message())
        time.sleep(60)

    except KeyboardInterrupt:
        next_step = input("Enter N for new or Q for Quit: ")
        if next_step == "N":
            state.Motor0.goTo(state.current_from_position)
            state.Motor1.goTo(state.current_from_position)
            wait_for_motors()
            print("Starting new session")
            continue

        closing_action()
        print("Ending now")
        break
