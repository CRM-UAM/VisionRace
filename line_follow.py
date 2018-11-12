import cv2
import numpy as np
import subprocess as sp
import time
import atexit
import sys
import signal
import psutil

from control_motores import *

Speed = 50

MotorsSetup()
BaseSpeed(Speed)

signal.signal(signal.SIGINT, signal_handler)

frames = [] # stores the video sequence for the demo

# Video capture parameters
(w, h) = (640,240)  # Resolution
bytesPerFrame = w * h
fps = 40 # setting to 250 will request the maximum framerate possible

lateral_search = 20 # number of pixels to search the line border
start_height = h - 5 # Scan index row 235

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
    frame.shape = (h,w) # set the correct dimensions for the numpy array for easier access to rows, now rows are columns

    start_time = time.clock()

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB) # Drawing color points requires RGB image
    # ret, thresh = cv2.threshold(frame, 105, 255, cv2.THRESH_BINARY)
    tresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

    signed_thresh = thresh[start_height].astype(np.int16) # select only one row
    diff = np.diff(signed_thresh)   #The derivative of the start_height line

    points = np.where(np.logical_or(diff > 200, diff < -200)) #maximums and minimums of derivative

    cv2.line(frame_rgb,(0,start_height),(640,start_height),(0,255,0),1) # draw horizontal line where scanning 

    if len(points) > 0 and len(points[0]) > 1: # if finds something like a black line
        if GetSpeed() == 0: # if is stopped but finds a line
            BaseSpeed(Speed)

        middle = (points[0][0] + points[0][1]) / 2

        cv2.circle(frame_rgb, (points[0][0], start_height), 2, (255,0,0), -1)
        cv2.circle(frame_rgb, (points[0][1], start_height), 2, (255,0,0), -1)
        cv2.circle(frame_rgb, (middle, start_height), 2, (0,0,255), -1)

        print(int((middle-320)/int(sys.argv[1])))
        Direction(int((middle - 320)/float(sys.argv[1])))
    else:
        start_height -= 5
	    start_height = start_height % h
        no_points_count += 1
	    Speed -= 0.1
	    BaseSpeed(Speed)
        if Speed <= 0:
            break        

    print("Loop took:", str((time.clock()- start_time) * 1000), 'ms')

    frames.append(frame_rgb)
    frames.append(thresh)	
    if psutil.virtual_memory().percent >= 85:
        del frames[0]

    if no_points_count > 50:
        print("Line lost")
        break

cleanup_finish()

def cleanup_finish():
    cameraProcess.terminate()
    MotorsStop()

    print("Writing frames to disk...")
    out = cv2.VideoWriter("drive_test.avi", cv2.cv.CV_FOURCC(*"MJPG"), 5, (w,h))

    for frame in frames:
        out.write(frame)

    out.release()

def signal_handler(sig, frame):
        print('Stop Everything!')
        cleanup_finish()
        sys.exit(0)