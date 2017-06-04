#!/usr/bin/python3

#run this script like a bash script
# ./line.py
#This way python3 interpreter is always used(if installed)

import cv2
import numpy as np
import time
import socket
import itertools

lateral_search = 20 # number of pixels to search the line border
start_left_margin = 100 # ignore the first 100 pixels
step = 1
start_height = -1

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Waiting for client to connect...")
sock.bind(("127.0.0.1", 8001))
sock.listen(1)

while True:
    conn, addr = sock.accept()
    break;

print("Connected from:", addr)

while True:
    data = conn.recv(50000)
    if data:
        start_time = time.clock()
        array = np.frombuffer(data, dtype='uint8')
        frame = cv2.imdecode(array, 1)
        imgray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY);
        ret, thresh = cv2.threshold(imgray, 110, 255, cv2.THRESH_BINARY)
        thresh_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
        shape = thresh.shape
        start_height = shape[0] - 1
        signed_thresh = thresh[start_height].astype(np.int16)
        diff = np.diff(signed_thresh)   #The derivative of the start_height line
        diff = diff[start_left_margin:] # ignore the first 100 values of the derivative
        left_list = []
        right_list = []
        points = np.where(np.logical_or(diff > 200, diff < -200)) #maximums and minimums of derivative

        if len(points[0]) > 0:
            for num in points[0]:
                cv2.circle(thresh_rgb, (num + start_left_margin, start_height), 2, (0,0,255), -1)

            last_x = points[0][0] + start_left_margin
            for altura in range(start_height - 1, 0, -step):
                if(thresh[altura][last_x] == 255): # if the pixel is while it means the line turned right
                    end_limit = last_x + lateral_search  # so we only search right

                    try:
                        index = np.where(thresh[altura][last_x:end_limit] == 0)[0][0] + last_x
                        left_list.append((index, altura))
                        last_x = index
                    except IndexError:
                        break;

                else: # if the pixel is black, the line turned left so we only search left
                    end_limit = last_x - lateral_search

                    try:
                        index = np.where(thresh[altura][end_limit:last_x] == 255)[0][-1] + end_limit
                        left_list.append((index, altura))
                        last_x = index
                    except IndexError:
                        break;
            if(len(points[0]) > 1):
                last_x = points[0][1] + start_left_margin
                for altura in range(start_height - 1, 0, -step):
                    if(thresh[altura][last_x] == 255): # if the pixel is white search left
                        end_limit = last_x - lateral_search
                        try:
                            index = np.where(thresh[altura][end_limit:last_x] == 0)[0][-1] + end_limit
                            right_list.append((index, altura))
                            last_x = index
                        except IndexError:
                            break;

                    else: # if the pixel is black search right
                        end_limit = last_x + lateral_search
                        try:
                            index = np.where(thresh[altura][last_x:end_limit] == 255)[0][0] + last_x
                            right_list.append((index, altura))
                            last_x = index
                        except IndexError:
                            break;

        print("Loop took:", str((time.clock()- start_time) * 1000), 'ms')


        for left, right in zip(left_list, right_list):
            cv2.circle(thresh_rgb, (int((left[0] + right[0]) / 2), left[1]), 2, (0,255,0), -1)
            cv2.circle(thresh_rgb, left, 2, (0,0,255 ), -1)
            cv2.circle(thresh_rgb, right, 2, (0,0,255 ), -1)

        conn.sendall( bytes(str(0).encode('utf8')) )
        cv2.imshow("Display Window", thresh_rgb)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

sock.close()
cv2.destroyAllWindows()
