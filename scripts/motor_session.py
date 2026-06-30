import time

import pandas as pd

import motor_state as state
from motor_utils import motor_reset, tide_control, time_elapsed, wait_for_motors
from motor_waves import wave_sequence
from paths import TIDE_DATA_CSV


def closing_action():
    state.Motor0.hardStop()
    state.Motor1.hardStop()
    time.sleep(1)
    while state.Motor0.getPosition() != state.Motor1.getPosition():
        state.Motor1.goTo(state.Motor0.getPosition())
        while state.Motor1.isBusy():
            continue
    print("loop ended")
    print(state.global_wave_timing)
    time.sleep(1)
    state.Motor0.setMaxSpeed(state.speed_steps_per_minute)
    state.Motor1.setMaxSpeed(state.speed_steps_per_minute)
    state.Motor0.goHome()
    state.Motor1.goHome()
    wait_for_motors()
    print(
        "Lowest_tide_at "
        + str(state.Motor0.getPosition())
        + " "
        + str(state.Motor1.getPosition())
    )
    time.sleep(2)
    state.Motor0.goTo(-state.lowest_tide)
    state.Motor1.goTo(-state.lowest_tide)
    wait_for_motors()
    state.Motor0.setCurrent(hold=0, run=0, acc=0, dec=0)
    state.Motor1.setCurrent(hold=0, run=0, acc=0, dec=0)
    print(
        "Motor 0 back home: "
        + str(state.Motor0.getPosition())
        + " Motor 1: "
        + str(state.Motor1.getPosition())
    )


def starting_act():
    state.Motor0.setCurrent(hold=100, run=100, acc=100, dec=100)
    state.Motor1.setCurrent(hold=100, run=100, acc=100, dec=100)

    state.Motor0.setDecel(120)
    state.Motor1.setDecel(120)
    state.Motor0.setAccel(120)
    state.Motor1.setAccel(120)

    state.Motor0.setMaxSpeed(state.speed_steps_per_minute)
    state.Motor1.setMaxSpeed(state.speed_steps_per_minute)

    state.Motor0.move(state.lowest_tide)
    state.Motor1.move(state.lowest_tide)
    wait_for_motors()
    state.Motor0.setAsHome()
    state.Motor1.setAsHome()
    print("At lowest tide level")
    time.sleep(1.5)

    state.Motor0.move(state.tide_range)
    state.Motor1.move(state.tide_range)
    wait_for_motors()
    print("At highest tide level")
    time.sleep(1.5)

    state.global_wave_timing = []
    state.tide_data = pd.read_csv(TIDE_DATA_CSV)
    state.time_of_new_tide_data = time.time()
    current_from = float(state.tide_data.tail(2).head(1)["Height"])
    current_to = float(state.tide_data.tail(2).tail(1)["Height"])
    state.current_from_position = round(current_from * state.tide_range)
    state.current_to_position = round(current_to * state.tide_range)
    state.previous_from_position = state.current_from_position
    state.previous_to_position = state.current_to_position
    state.tide_distance_count = state.current_to_position - state.current_from_position
    time.sleep(0.5)
    state.Motor0.goTo(state.current_from_position)
    state.Motor1.goTo(state.current_from_position)
    wait_for_motors()
    time.sleep(0.5)
    wave_sequence(tide_distance=0, number_of_waves=1)
    time.sleep(1)


def tide_data_refresh():
    state.previous_from_position = state.current_from_position
    state.previous_to_position = state.current_to_position
    state.Motor0.setCurrent(hold=100, run=100, acc=100, dec=100)
    state.Motor1.setCurrent(hold=100, run=100, acc=100, dec=100)

    while True:
        try:
            state.tide_data = pd.read_csv(TIDE_DATA_CSV)
            break
        except (OSError, pd.errors.EmptyDataError) as error:
            print(f"Waiting for tide data: {error}")
            time.sleep(5)

    current_from = tide_control(float(state.tide_data.tail(2).head(1)["Height"]))
    current_to = tide_control(float(state.tide_data.tail(2).tail(1)["Height"]))
    state.current_from_position = round(current_from * state.tide_range)
    state.current_to_position = round(current_to * state.tide_range)
    print("Actual From (m): " + str(current_from) + " Actual To (m): " + str(current_to))
    print(
        "Motor Position From : "
        + str(state.current_from_position)
        + " Motor Position To : "
        + str(state.current_to_position)
    )
    state.tide_distance_count = state.current_to_position - state.current_from_position

    if (
        state.current_from_position != state.previous_from_position
        and state.current_to_position != state.previous_to_position
    ):
        state.time_of_new_tide_data = time.time()
        if abs(state.Motor0.getPosition() - state.current_from_position) != 0 or (
            abs(state.Motor1.getPosition() - state.current_from_position) != 0
        ):
            coverup_distance = state.current_from_position - state.Motor0.getPosition()
            wave_sequence(number_of_waves=5, tide_distance=coverup_distance)
    elif state.current_to_position == state.previous_to_position:
        if (
            abs(state.Motor0.getPosition() - state.current_to_position) == 0
            or abs(state.Motor1.getPosition() - state.current_to_position) == 0
        ):
            wave_sequence(tide_distance=0)
        else:
            try:
                target_distance = state.current_to_position - state.Motor0.getPosition()
                waves_in_remaining_time = round(
                    (900 - time_elapsed(state.time_of_new_tide_data))
                    / state.global_wave_timing[-1][-1]
                )
                tide_pace = round(target_distance / waves_in_remaining_time)
                wave_sequence(tide_distance=tide_pace)
            except (IndexError, KeyError, ZeroDivisionError, TypeError):
                print("Error in standard wave. Running blank wave to kill time...")
                closing_action()
                time.sleep(30)
                starting_act()
