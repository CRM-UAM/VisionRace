#!/usr/bin/python3

#run this script like a bash script
# ./line.py
#This way python3 interpreter is always used(if installed)

import cv2
import numpy as np
import subprocess as sp
import time
import atexit

frames = [] # stores the video sequence for the demo
max_frames = 300

N_frames = 0

# Video capture parameters
(w, h) = (640,240)
bytesPerFrame = w * h
fps = 250 # setting to 250 will request the maximum framerate possible

lateral_search = 20 # number of pixels to search the line border
start_height = h - 2 # The first line sometimes might contain artifacts
start_left_margin = 100 # ignore the first 100 pixels
step = 1

# "raspividyuv" is the command that provides camera frames in YUV format
#  "--output -" specifies stdout as the output
#  "--timeout 0" specifies continuous video
#  "--luma" discards chroma channels, only luminance is sent through the pipeline
# see "raspividyuv --help" for more information on the parameters
videoCmd = "raspividyuv -w "+str(w)+" -h "+str(h)+" --output - --timeout 0 --framerate "+str(fps)+" --luma --nopreview"
videoCmd = videoCmd.split() # Popen requires that each parameter is a separate string

cameraProcess = sp.Popen(videoCmd, stdout = sp.PIPE) # start the camera
atexit.register(cameraProcess.terminate) # this closes the camera process in case the python scripts exits unexpectedly

# wait for the first frame and discard it (only done to measure time more accurately)
rawStream = cameraProcess.stdout.read(bytesPerFrame)

print("Recording...")

while True:
    cameraProcess.stdout.flush() # discard any frames that we were not able to process in time
    # Parse the raw stream into a numpy array
    frame = np.fromfile(cameraProcess.stdout, count=bytesPerFrame, dtype=np.uint8)
    if frame.size != bytesPerFrame:
        print("Error: Camera stream closed unexpectedly")
        break
    frame.shape = (h,w) # set the correct dimensions for the numpy array
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB) # Drawing color points requires RGB image
    start_time = time.clock()

    ret, thresh = cv2.threshold(imgray, 100, 255, cv2.THRESH_BINARY)
    signed_thresh = thresh[start_height].astype(np.int16)
    diff = np.diff(signed_thresh)   #The derivative of the start_height line
    diff = diff[start_left_margin:] # ignore the first 100 values of the derivative

    points = np.where(np.logical_or(diff > 200, diff < -200)) #maximums and minimums of derivative

    if len(points[0]) > 0:
        for num in points[0]:
            cv2.circle(frame_rgb, (num + start_left_margin, start_height), 2, (0,0,255), -1)

        #Left side
        last_x = points[0][0] + start_left_margin
        for altura in range(start_height - 1, 0, -step):
            if(thresh[altura][last_x] == 255): # if the pixel is while it means the line turned right
                end_limit = last_x + lateral_search  # so we only search right

                try:
                    index = np.where(thresh[altura][last_x:end_limit] == 0)[0][0] + last_x
                    point_list.append((index, altura))
                    last_x = index
                except IndexError:
                    break;

            else: # if the pixel is black, the line turned left so we only search left
                end_limit = last_x - lateral_search

                try:
                    index = np.where(thresh[altura][end_limit:last_x] == 255)[0][-1] + end_limit
                    point_list.append((index, altura))
                    last_x = index
                except IndexError:
                    break;

        #right side
        if(len(points[0]) > 1):
            last_x = points[0][1] + start_left_margin
            for altura in range(start_height - 1, 0, -step):
                if(thresh[altura][last_x] == 255): # if the pixel is white search left
                    end_limit = last_x - lateral_search
                    try:
                        index = np.where(thresh[altura][end_limit:last_x] == 0)[0][-1] + end_limit
                        point_list.append((index, altura))
                        last_x = index
                    except IndexError:
                        break;

                else: # if the pixel is black search right
                    end_limit = last_x + lateral_search
                    try:
                        index = np.where(thresh[altura][last_x:end_limit] == 255)[0][0] + last_x
                        point_list.append((index, altura))
                        last_x = index
                    except IndexError:
                        break;
    print("Loop took:", str((time.clock()- start_time) * 1000), 'ms')

    #draw all points in the list
    for point in point_list:
        cv2.circle(frame_rgb, point, 2, (255,0,0), -1)

    #show the frame
    cv2.imshow("Display Window", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cameraProcess.terminate() # stop the camera
cv2.destroyAllWindows()
