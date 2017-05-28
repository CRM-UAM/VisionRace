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
                cv2.circle(t_img, (num + start_left_margin, start_height), 2, (255,0,0), -1)

            #Left side
            last_x = points[0][0] + start_left_margin
            for altura in range(start_height - 1, 0, -1):
                if(thresh[altura][last_x] == 255):
                    end_limit = last_x + lateral_search
                    if (end_limit) > 1280:
                        end_limit = 1279
                    for num in range(last_x, end_limit, 1):
                        if thresh[altura][num] == 0:
                            point_list.append((num, altura))
                            last_x = num
                            break
                    else:
                        break
                elif(thresh[altura][last_x] == 0):
                    end_limit = last_x - lateral_search
                    if (end_limit) < 0:
                        end_limit = 0

                    for num in range(last_x, end_limit, -1):
                        if thresh[altura][num] == 255:
                            point_list.append((num, altura))
                            last_x = num
                            break
                    else:
                        break

            #right side
            if(len(points[0]) > 1):
                last_x = points[0][1] + start_left_margin
                for altura in range(start_height - 1, 0, -1):
                    if(thresh[altura][last_x] == 255):
                        end_limit = last_x - lateral_search
                        if (end_limit) < 0:
                            end_limit = 0
                        for num in range(last_x, end_limit, -1):
                            if thresh[altura][num] == 0:
                                point_list.append((num, altura))
                                last_x = num
                                break
                        else:
                            break
                    elif(thresh[altura][last_x] == 0):
                        end_limit = last_x + lateral_search
                        if (end_limit) > 1280:
                            end_limit = 1279
                        for num in range(last_x, end_limit, 1):
                            if thresh[altura][num] == 255:
                                point_list.append((num, altura))
                                last_x = num
                                break
                        else:
                            break

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
