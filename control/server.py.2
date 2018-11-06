import socket
import sys
import time
import atexit
import thread
import MotorControl
from MotorControl import MotorsSetup, MotorsStop, Direction, BaseSpeed

# Medidas en % por segundo
MAX_SPEED_FORWARD = 80
MAX_SPEED_REVERSE = 50
MAX_STEERING = 100
STEERING_SPEED = 50
STEERING_AUTOCENTER = 80
ACCELERATION = 25
NEGATIVE_ACCELERATION = 30
NO_THROTTLE_ACCELERATION = 15

speed = 0
steering_angle = 0

#timing
delta_time = 0
last_time = 0

def on_quit():
	sock.close()
	MotorsStop()
	print "Socket Closed"

atexit.register(on_quit)

data = "0000" # "[w][a][s][d]"

def ChangeMotorsState():
	global speed, steering_angle
	BaseSpeed(speed)
	Direction(steering_angle)

def SetSpeed():
	global delta_time, last_time, speed, steering_angle
	while True:
		now = time.clock()
		delta_time = now - last_time
		last_time = now

		# Control de la velocidad
		if data[0] == "1":
			if speed < MAX_SPEED_FORWARD:
				speed += ACCELERATION * delta_time
		elif data[2] != "1":
			if speed > 0:
				speed -= NO_THROTTLE_ACCELERATION * delta_time

		if data[2] == "1":
			if speed > -MAX_SPEED_REVERSE:
				speed -= NEGATIVE_ACCELERATION * delta_time
		elif data[0] != "1":
			if speed < 0:
				speed += NO_THROTTLE_ACCELERATION * delta_time

		# Control de la direccion
		if data[1] == "1":
			if steering_angle > -MAX_STEERING:
				steering_angle -= STEERING_SPEED * delta_time
		elif data[3] != "1":
			if steering_angle < 0:
				steering_angle += STEERING_AUTOCENTER * delta_time

		if data[3] == "1":
			if steering_angle < MAX_STEERING:
				steering_angle += STEERING_SPEED * delta_time
		elif data[1] != "1":
			if steering_angle > 0:
				steering_angle -= STEERING_AUTOCENTER * delta_time

		ChangeMotorsState()


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Socket ceated"

server_address = ('0.0.0.0', 9123)
sock.bind(server_address)

sock.listen(1)
print "Waiting for client to connect"

connection, client_address = sock.accept()
print "Connected from {}".format(client_address)
thread.start_new_thread(SetSpeed, ())
MotorsSetup()

while True:
	tmp = connection.recv(4)
	if tmp:
	   data = tmp
	   print data
	else:
	    break

connection.close()
sock.close()
