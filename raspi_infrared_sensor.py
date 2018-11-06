#!/usr/bin/python2

#run this script like a bash script
# ./line.py
#This way python3 interpreter is always used(if installed)

import cv2
import numpy as np
import subprocess as sp
import time
import atexit
import sys

from control_motores_inv import *

def nothing(x):
    pass

Speed = -80

MotorsSetup()
BaseSpeed(Speed)

frames = []

frames = [] # stores the video sequence for the demo
max_frames = 300

N_frames = 0
#cv2.namedWindow('Thresh Window')
#cv2.createTrackbar('Thresh', 'Thresh Window', 20, 200, nothing)

# Video capture parameters
(w, h) = (640,240)
bytesPerFrame = w * h
fps = 40 # setting to 250 will request the maximum framerate possible

lateral_search = 20 # number of pixels to search the line border
start_height = h - 5 # The first line sometimes might contain artifacts
start_left_margin = 100 # ignore the first 100 pixels
step = 1

# "raspividyuv" is the command that provides camera frames in YUV format
#  "--output -" specifies stdout as the output
#  "--timeout 0" specifies continuous video
#  "--luma" discards chroma channels, only luminance is sent through the pipeline
# see "raspividyuv --help" for more information on the parameters
videoCmd = "raspividyuv -w "+str(w)+" -h "+str(h)+" --output - --timeout 0 -vs -co 50 -br 50 --framerate "+str(fps)+" --luma --nopreview"
videoCmd = videoCmd.split() # Popen requires that each parameter is a separate string

cameraProcess = sp.Popen(videoCmd, stdout = sp.PIPE) # start the camera
atexit.register(cameraProcess.terminate) # this closes the camera process in case the python scripts exits unexpectedly

# wait for the first frame and discard it (only done to measure time more accurately)
rawStream = cameraProcess.stdout.read(bytesPerFrame)

print("Recording...")

no_points_count = 0

while True:
#for qwerty in xrange(500):
    cameraProcess.stdout.flush() # discard any frames that we were not able to process in time
    # Parse the raw stream into a numpy array
    frame = np.fromfile(cameraProcess.stdout, count=bytesPerFrame, dtype=np.uint8)
    if frame.size != bytesPerFrame:
        print("Error: Camera stream closed unexpectedly")
        break
    frame.shape = (h,w) # set the correct dimensions for the numpy array

    start_time = time.clock()

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB) # Drawing color points requires RGB image
    ret, thresh = cv2.threshold(frame, 105, 255, cv2.THRESH_BINARY)
    #ret, thresh = cv2.threshold(frame, cv2.getTrackbarPos('Thresh','Thresh Window'), 255, cv2.THRESH_BINARY)

    signed_thresh = thresh[start_height].astype(np.int16)
    diff = np.diff(signed_thresh)   #The derivative of the start_height line
    #diff = diff[start_left_margin:] # ignore the first 100 values of the derivative
    point_list = []
    points = np.where(np.logical_or(diff > 200, diff < -200)) #maximums and minimums of derivative
    #if len(points[0])>1 and diff[points[0][0]] == 255:
        #points = np.delete(points, 0)

    cv2.line(frame_rgb,(0,start_height),(640,start_height),(0,255,0),1)
    #print(points)
    if len(points) > 0 and len(points[0]) > 1:
        if GetSpeed() == 0:
            BaseSpeed(Speed)
        middle = (points[0][0] + points[0][1]) / 2
        cv2.circle(frame_rgb, (points[0][0], start_height), 2, (255,0,0), -1)
        cv2.circle(frame_rgb, (points[0][1], start_height), 2, (255,0,0), -1)
        cv2.circle(frame_rgb, (middle, start_height), 2, (0,0,255), -1)
        print(int((middle-320)/int(sys.argv[1])))
        Direction(int((middle - 320)/float(sys.argv[1])))
    else:
        start_height -= 5
        no_points_count += 1

    print("Loop took:", str((time.clock()- start_time) * 1000), 'ms')

    frames.append(frame_rgb)
    #frames.append(thresh)	
    if len(frames) == 26:
        del frames[0]

    if no_points_count > 20:
        print("Line lost")
        #break

    #show the frame
    #cv2.imshow("Display Window", frame_rgb)
    #cv2.imshow("Thresh Window", thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cameraProcess.terminate() # stop the camera
cv2.destroyAllWindows()
MotorsStop()

print("Writing frames to disk...")
out = cv2.VideoWriter("drive_test.avi", cv2.cv.CV_FOURCC(*"MJPG"), 30, (w,h))
for n in xrange(len(frames)):
    #cv2.imwrite("frame"+str(n)+".png", frames[n]) # save frame as a PNG image
    #thresh_rgb = cv2.cvtColor(frames[n],cv2.COLOR_GRAY2RGB) # video codec requires RGB image
    out.write(frames[n])
    #out.write(thresh_rgb)
out.release()
