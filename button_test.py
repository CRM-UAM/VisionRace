import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BOARD)

GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(38)
    if input_state == False:
        print('Button Pressed')
        os.system('python Main.py 4')
	time.sleep(0.2)
