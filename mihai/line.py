#!/usr/bin/python3

#run this script like a bash script
# ./line.py
#This way python3 interpreter is always used(if installed)

import numpy as np
import sys
import cv2
import time

filename = ""
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print("No video file\n Use: python", sys.argv[0], "someVideoFile.mp4")
    exit(1)

vidFile = cv2.VideoCapture(filename)

#retval, image = cv2.imread('first_test.jpg')

lateral_search = 20
start_height = 719
start_left_margin = 100 # ignore the first 100 pixels
step = 3
while True:
    time_1 = time.clock()
    succesfully_read, image = vidFile.read()
    if succesfully_read:
        point_list = []
        imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 100, 255, cv2.THRESH_BINARY)
        signed_thresh = thresh[start_height].astype(np.int16)
        diff = np.diff(signed_thresh)   #defivada
        diff = diff[start_left_margin:]
        t_img = image
        points = np.where(np.logical_or(diff > 200, diff < -200)) #maximums and minimums of derivative

        if len(points[0]) > 0:
            for num in points[0]:
                cv2.circle(t_img, (num + start_left_margin, start_height), 2, (0,0,255), -1)

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

        print(str((time.clock()- time_1) * 1000), 'ms')

        #draw all points in the list
        for point in point_list:
            cv2.circle(t_img, point, 2, (255,0,0), -1)

        #show the frame
        cv2.imshow("Display Window", t_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
