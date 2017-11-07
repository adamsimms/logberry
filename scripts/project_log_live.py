#import the required module
import Slush
import time
import tide_data as tide
import wave_data as wave
import pandas as pd
import numpy as np


#fresh data
tide.get_tide_data()
wave.get_wave_data()

#initalizes the board and all its functions
SlushEngine = Slush.sBoard()

#initalizes the motor on the board
Motor0 = Slush.Motor(0)
Motor1 = Slush.Motor(3)

def motorReset(Motor_name = Motor0):
    Motor_name.resetDev()
    Motor_name.setMicroSteps(1)
    Motor_name.free()

def off(Motor_name = Motor0):
    motorReset(Motor_name)
    Motor_name.setCurrent(hold = 0, run = 0, acc =0, dec = 0)


def create_wave(first_motor = Motor0, second_motor = Motor1, wave_height = 250, wave_diff = 25, max_count = 10, current_count = 0, sleep_delay = .2, speed = 900):
    first_motor.setMaxSpeed(speed)
    Motor1.setMaxSpeed(speed)
    while current_count < max_count:
        current_count += 1
        while (first_motor.isBusy()):
            continue
        first_motor.move(wave_height)
        if current_count >= 1:
            time.sleep(sleep_delay)
        while (second_motor.isBusy()):
            continue
        second_motor.move(wave_height)
        while True:
            if first_motor.isBusy() == False:
                first_motor.move(-1*(wave_height-wave_diff))
                time.sleep(sleep_delay)
                while True:
                    if second_motor.isBusy() == False:
                        second_motor.move(-1*(wave_height-wave_diff))
                        break
                break
        while (first_motor.isBusy()#|second_motor.isBusy()
               ):
                continue
            
def cmToStep(cm):
     return(round(cm*5400/9))

def sleepDelayCount(step):
    step = abs(step)
    if (step < 850):
        return .3
    elif (step >=850) & (step <=1000):
        return .35
    elif (step > 1000) & (step < 1300):
        return .4
    elif (step >= 1300) & (step < 1450):
        return .45
    elif (step >= 1450) & (step < 1600):
        return .5
    else:
        return .6

def time_elapsed(time_value):
    return(time.time()-time_value)


def wave_sequence(tide_distance, number_of_waves = 1):
    loop_count = 0
    wave_data = pd.read_csv("wave_status.csv")
    max_wave_height = round(cmToStep(cm = float(wave_data['max_wave_height'][0]))*.8)*multiplier
    sig_wave_height = round(cmToStep(cm = float(wave_data['sig_wave_height'][0]))*.8)*multiplier
    peak_wave_period = wave_data['peak_wave_period'][0]
    print(peak_wave_period)
    diff_per_wave = round(tide_distance/number_of_waves)
    wave_timing = []
    while loop_count < number_of_waves:
        start_time = time.time()
        
        create_wave(wave_height = max_wave_height, wave_diff = round(max_wave_height*.2), max_count = 1, current_count = 0, sleep_delay = sleepDelayCount(max_wave_height), speed = 1000)
        if time.time()-start_time > peak_wave_period:
            create_wave(wave_height = sig_wave_height, wave_diff = diff_per_wave-round(max_wave_height*.2), max_count = 1, current_count = 0, sleep_delay = sleepDelayCount(diff_per_wave-round(max_wave_height*.2)), speed = 1000)
            loop_count += 1
            wave_timing.append(time_elapsed(start_time))
            continue
        
        create_wave(wave_height = round(max_wave_height*.8), wave_diff = -(round(max_wave_height*.2*.8)), max_count = 1, current_count = 0, sleep_delay = sleepDelayCount(round(max_wave_height*.8)), speed = 1000)
        if time.time()-start_time > peak_wave_period:
            create_wave(wave_height = sig_wave_height, wave_diff = diff_per_wave-(round(max_wave_height*.2*.2)), max_count = 1, current_count = 0, sleep_delay = sleepDelayCount(diff_per_wave-(round(max_wave_height*.2*.2))), speed = 1000)
            loop_count += 1
            wave_timing.append(time_elapsed(start_time))
            continue
        
        create_wave(wave_height = sig_wave_height, wave_diff = -(round(max_wave_height*.2*.2)), max_count = 1, current_count = 0, sleep_delay = sleepDelayCount(sig_wave_height), speed = 1000)
        if time.time()-start_time > peak_wave_period:
            create_wave(wave_height = sig_wave_height, wave_diff = diff_per_wave, max_count = 1, current_count = 0, sleep_delay = sleepDelayCount(diff_per_wave), speed = 1000)
            loop_count += 1
            wave_timing.append(time_elapsed(start_time))
            continue
        
        create_wave(wave_height = round(sig_wave_height*.8), wave_diff = 0, max_count = 1, current_count = 0, sleep_delay = sleepDelayCount(round(sig_wave_height*.8)), speed = 1000)
        if time.time()-start_time > peak_wave_period:
            create_wave(wave_height = sig_wave_height, wave_diff = diff_per_wave, max_count = 1, current_count = 0, sleep_delay = sleepDelayCount(diff_per_wave), speed = 1000)
            loop_count += 1
            wave_timing.append(time_elapsed(start_time))
            continue
        
        create_wave(wave_height = round(sig_wave_height*.8), wave_diff = diff_per_wave, max_count = 1, current_count = 0, sleep_delay = sleepDelayCount(max_wave_height), speed = 1000)
        
        wave_timing.append(time_elapsed(start_time))
        
        if time_elapsed(start_time) < (peak_wave_period-(.8)):
            time_to_kill = (peak_wave_period - time_elapsed(start_time))
            time_killing_start = time.time()
            while (time_to_kill*.8) > time_elapsed(time_killing_start):
                create_wave(wave_height = round(sig_wave_height*.8), wave_diff = 0, max_count = 1, current_count = 0, sleep_delay = sleepDelayCount(round(sig_wave_height*.8)), speed = 1000)
        loop_count += 1
        #print("After "+str(loop_count)+" waves: \n Motor 0 : "+str(Motor0.getPosition())+" Motor 1: "+str(Motor1.getPosition()))
    while (Motor1.isBusy()):
        continue   
    print("Motor 0 after all waves: "+str(Motor0.getPosition())+" Motor 1: "+str(Motor1.getPosition()))
    print(wave_timing)
    print(np.mean(wave_timing))
    global_wave_timing.append(wave_timing)

def tide_control(value):
    if value > 1.1:
        return float(1.1)
    elif value < -0.1:
        return float(-0.1)
    else:
        return float(value)

def tide_data_refresh():
    global tide_data
    global previous_from_position
    global previous_to_position
    global current_from_position
    global current_to_position
    global tide_distance_count
    global time_of_new_tide_data
    (previous_from_position, previous_to_position) = (current_from_position, current_to_position)
    while True:
        try:
            tide_data = pd.read_csv('tide_data.csv')
            break
        except:
            continue
    (current_from, current_to) = (tide_control(float(tide_data.tail(2).head(1)['Height'])), tide_control(float(tide_data.tail(2).tail(1)['Height'])))
    (current_from_position, current_to_position) = (round(current_from*18000), round(current_to*18000))
    print('From : '+str(current_from_position)+' To : '+str(current_to_position))
    tide_distance_count = current_to_position - current_from_position
    
    if (current_from_position != previous_from_position) & (current_to_position != previous_to_position):
        time_of_new_tide_data = time.time()
        if (abs(Motor0.getPosition() - current_from_position) != 0)|(abs(Motor1.getPosition() - current_from_position) != 0):
            coverup_distance = current_from_position - Motor0.getPosition()
            wave_sequence(number_of_waves = 5, tide_distance = coverup_distance)
    elif (current_to_position == previous_to_position):
        if abs(Motor0.getPosition() - current_to_position) == 0|abs(Motor1.getPosition() - current_to_position) == 0:
            wave_sequence(tide_distance = 0)
        else:
            target_distance = current_to_position - Motor0.getPosition()
            try:
                waves_in_remaining_time = round((900-time_elapsed(time_of_new_tide_data))/global_wave_timing[-1][-1])
                tide_pace = round(target_distance/waves_in_remaining_time)
                wave_sequence(tide_distance = tide_pace)
            except:
                pass




#inputs
lowest_tide = cmToStep(eval(input("Enter height of lowest tide from ground in cm :(test = 2)")))
tide_range = cmToStep(eval(input("Enter height between lowest tide and highest tide in cm (test = 30) :")))
multiplier = eval(input("Enter wave multiplier: "))

#SCRIPT OF EVENTS
#start and position motor    
motorReset(Motor0)
motorReset(Motor1)
Motor0.setMaxSpeed(1000)
Motor1.setMaxSpeed(1000)

Motor0.move(lowest_tide)
Motor1.move(lowest_tide)
while (Motor0.isBusy()|Motor1.isBusy()):
    continue
Motor0.setAsHome()
Motor1.setAsHome()


#Load tide data to reach current tide position 
global_wave_timing = [] 
tide_data = pd.read_csv('tide_data.csv')
time_of_new_tide_data = time.time()
(current_from, current_to) = (float(tide_data.tail(2).head(1)['Height']), float(tide_data.tail(2).tail(1)['Height']))
(current_from_position, current_to_position) = (round(float(current_from)*tide_range), round(float(current_to)*tide_range))
(previous_from_position, previous_to_position) = (current_from_position, current_to_position)
tide_distance_count = current_to_position - current_from_position
time.sleep(.5)
Motor0.goTo(current_from_position)
Motor1.goTo(current_from_position)
while (Motor0.isBusy()|Motor1.isBusy()):
    continue
time.sleep(.5)
wave_sequence(tide_distance = 0, number_of_waves = 1)
time.sleep(1)






###MAIN ACTION
try:
    while True:
        tide_data_refresh()
finally:
#except KeyboardInterrupt:
    print("loop ended")
    print(global_wave_timing)
    time.sleep(1)
    Motor0.setMaxSpeed(800)
    Motor1.setMaxSpeed(800)
    Motor0.goHome()
    Motor1.goHome()
    while (Motor0.isBusy()|Motor1.isBusy()):
        continue
    print("Lowest_tide_at "+str(Motor0.getPosition())+" "+str(Motor1.getPosition()))
    time.sleep(2)
    Motor0.goTo(-lowest_tide)
    Motor1.goTo(-lowest_tide)
    while (Motor0.isBusy()|Motor1.isBusy()):
        continue
    print("Motor 0 back home: "+str(Motor0.getPosition())+" Motor 1: "+str(Motor1.getPosition()))


    Motor0.setCurrent(hold = 0, run = 0, acc =0, dec = 0)
    Motor1.setCurrent(hold = 0, run = 0, acc =0, dec = 0)
