import socket
import sys
import os

import numpy as np
import cv2

from ImageProcessing import ImProcess

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 8001) # CHANGE THIS ARGUMENTS
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    connection, client_address = sock.accept()

    try:

        while True:
            data = connection.recv(50000)

            if data:
                array = np.frombuffer(data, dtype='uint8') #Read the buffer from the TCP connection
                img = cv2.imdecode(array, 1) # Decode the image to fit the OpenCV model
                if img is not None:
                    fm, d = ImProcess(img) #Call the function from ImageProcessing
                    cv2.imshow("window", fm) # Show visual debug (Comment this line for performance increase)
                    connection.sendall( bytes(str(d).encode('utf8')) ) #Send back to simulator the direction integer
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            else:
                break
            
    finally:
        # Clean up the connection
        cv2.destroyAllWindows()
        connection.close()