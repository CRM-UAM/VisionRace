import socket
import sys
import os
import numpy as np
import pdb

import cv2
import time

from Image import *
from Utils import *

font = cv2.FONT_HERSHEY_SIMPLEX
direction = 0
Images=[]
N_SLICES = 4

for q in range(N_SLICES):
    Images.append(Image())

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 8001)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    connection, client_address = sock.accept()

    try:
        while True:
            data = connection.recv(50000)

            if data:
                array = np.frombuffer(data, dtype='uint8')
                img = cv2.imdecode(array, 1)
                direction = 0
                img = RemoveBackground(img, False)
                if img is not None:
                    t1 = time.clock()
                    SlicePart(img, Images, N_SLICES)
                    for i in range(N_SLICES):
                        direction += Images[i].dir
                    
                    fm = RepackImages(Images)
                    t2 = time.clock()
                    cv2.putText(fm,"Time: " + str((t2-t1)*1000) + " ms",(10, 470), font, 0.5,(0,0,255),1,cv2.LINE_AA)
                    cv2.imshow("Vision Race", fm)
                    connection.sendall( bytes(str(direction).encode('utf8')) )
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            else:
                break
            
    finally:
        # Clean up the connection
        cv2.destroyAllWindows()
        connection.close()