import RPi.GPIO as GPIO
import time

def L_Speed(speed):
    if speed < 0:
        GPIO.output(L_DIR_PIN, GPIO.HIGH)
    else:
        GPIO.output(L_DIR_PIN, GPIO.LOW)

    speed = abs(speed)
    if speed > 100:
        speed = 100

    L_MOTOR.ChangeDutyCycle(speed)

def R_Speed(speed):
    if speed < 0:
        GPIO.output(R_DIR_PIN, GPIO.HIGH)
    else:
        GPIO.output(R_DIR_PIN, GPIO.LOW)

    speed = abs(speed)
    if speed > 100:
        speed = 100

    R_MOTOR.ChangeDutyCycle(speed)


L_PWM_PIN = 16
L_DIR_PIN = 15

R_PWM_PIN = 12
R_DIR_PIN = 11

GPIO.setmode(GPIO.BOARD)

GPIO.setup(L_PWM_PIN, GPIO.OUT)
GPIO.setup(L_DIR_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(R_PWM_PIN, GPIO.OUT)
GPIO.setup(R_DIR_PIN, GPIO.OUT, initial=GPIO.LOW)

L_MOTOR = GPIO.PWM(L_PWM_PIN, 1000)
L_MOTOR.start(0)

R_MOTOR = GPIO.PWM(R_PWM_PIN, 1000)
R_MOTOR.start(0)
"""
for x in xrange(0,100, 5):
    L_MOTOR.ChangeDutyCycle(x)
    R_MOTOR.ChangeDutyCycle(x)
    time.sleep(1)
"""

L_Speed(20)
R_Speed(20)

#x = input("Speed ")
#y = input("Sense ")

#Speed(L_MOTOR, int(x), int(y))

time.sleep(15)

L_MOTOR.stop()
R_MOTOR.stop()
GPIO.cleanup()
