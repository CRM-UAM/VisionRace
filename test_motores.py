import time
from control_motores import *

MotorsSetup()

BaseSpeed(100)
print("ACCEL")

Direction(25)
time.sleep(29)

MotorsStop()
print("STOP")
