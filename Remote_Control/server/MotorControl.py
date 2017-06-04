import RPi.GPIO as GPIO
import time

SPEED = 10

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
R_MOTOR = GPIO.PWM(R_PWM_PIN, 1000)

def MotorsSetup():
	L_MOTOR.start(0)
	R_MOTOR.start(0)

def L_Speed(speed):
    GPIO.output(L_DIR_PIN, int(speed < 0))
    speed = abs(speed)
    if speed > 100:
        speed = 100
    elif speed < -100:
	speed = -100

    L_MOTOR.ChangeDutyCycle(speed)

def R_Speed(speed):
    GPIO.output(R_DIR_PIN, int(speed < 0))
    speed = abs(speed)
    if speed > 100:
        speed = 100
    elif speed < -100:
	speed = -100

    R_MOTOR.ChangeDutyCycle(speed)

def Direction(difference):
	L_Speed(SPEED+difference)
	R_Speed(SPEED-difference)

def BaseSpeed(speed):
	global SPEED
	SPEED = speed
	L_Speed(SPEED)
	R_Speed(SPEED)

def GetSpeed():
	global SPEED
	return SPEED

def MotorsStop():
	L_MOTOR.stop()
	R_MOTOR.stop()
	GPIO.cleanup()
