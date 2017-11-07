#import the required module
import Slush
import time
def cmToStep(cm):
     return(round(cm*5400/9))
    
movement = eval(input("Enter (left_motor_in_cm,right_motor_in_cm): "))
m0_steps = cmToStep(float(movement[0]))
m1_steps = cmToStep(float(movement[1]))
#initalizes the board and all its functions
SlushEngine = Slush.sBoard()

#initalizes the motor on the board
Motor0 = Slush.Motor(0)
Motor1 = Slush.Motor(3)

def motorReset(Motor_name = Motor0):
    Motor_name.resetDev()
#    Motor_name.setCurrent(hold = 200, run = 200, acc =200, dec = 200)
    Motor_name.setMicroSteps(1)
    Motor_name.free()

motorReset(Motor0)
motorReset(Motor1)
Motor0.setAsHome()
Motor1.setAsHome()

cm = 5400/9
lowest_tide = round(.05*cm)
Motor0.setMaxSpeed(800)
Motor1.setMaxSpeed(800)
Motor0.move(m0_steps)
Motor1.move(m1_steps)

while (Motor0.isBusy()|Motor1.isBusy()):
    continue


Motor0.setCurrent(hold = 0, run = 0, acc =0, dec = 0)
Motor1.setCurrent(hold = 0, run = 0, acc =0, dec = 0)
