import time
from control_motores import *

MotorsSetup()

BaseSpeed(100)
print("100")
time.sleep(3)

#Direction(25)
#time.sleep(29)

MotorsStop()
print("STOP")
