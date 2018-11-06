# Fast reading from the raspberry camera with Python, Numpy, and OpenCV
# Allows to process grayscale video up to 124 FPS (tested in Raspberry Zero Wifi with V2.1 camera)
#
# Made by @CarlosGS in May 2017
# Club de Robotica - Universidad Autonoma de Madrid
# http://crm.ii.uam.es/
# License: Public Domain, attribution appreciated

import cv2
import numpy as np
import subprocess as sp
import time
import atexit

frames = [] # stores the video sequence for the demo
max_frames = 300

N_frames = 0

# Video capture parameters
(w,h) = (640,240)

DIV = 8
sl = 240 / DIV

bytesPerFrame = w * h
fps = 40 # setting to 250 will request the maximum framerate possible

# "raspividyuv" is the command that provides camera frames in YUV format
#  "--output -" specifies stdout as the output
#  "--timeout 0" specifies continuous video
#  "--luma" discards chroma channels, only luminance is sent through the pipeline
# see "raspividyuv --help" for more information on the parameters
videoCmd = "raspividyuv -w "+str(w)+" -h "+str(h)+" --output - --timeout 0 --framerate "+str(fps)+" --luma --nopreview"
videoCmd = videoCmd.split() # Popen requires that each parameter is a separate string

cameraProcess = sp.Popen(videoCmd, stdout=sp.PIPE) # start the camera
atexit.register(cameraProcess.terminate) # this closes the camera process in case the python scripts exits unexpectedly

# wait for the first frame and discard it (only done to measure time more accurately)
rawStream = cameraProcess.stdout.read(bytesPerFrame)

print("Recording...")

start_time = time.time()

while True:
    	cameraProcess.stdout.flush() # discard any frames that we were not able to process in time
    # Parse the raw stream into a numpy array
    	frame = np.fromfile(cameraProcess.stdout, count=bytesPerFrame, dtype=np.uint8)
    	if frame.size != bytesPerFrame:
        	print("Error: Camera stream closed unexpectedly")
        	break
    	frame.shape = (h,w) # set the correct dimensions for the numpy array

    # The frame can be processed here using any function in the OpenCV library.

    # Full image processing will slow down the pipeline, so the requested FPS should be set accordingly.
    #frame = cv2.Canny(frame, 50,150)

	ret, thresh = cv2.threshold(frame,100,255,cv2.THRESH_BINARY_INV)
	frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
	altura, anchura = frame.shape[:2]
	sl = altura / DIV
	centers = []
	for i in xrange(1, DIV+1):
	        altura = (i*sl)-1
        	diff = np.diff(thresh[altura], n=2)
        	inx = np.where(diff > 200)[0]
        	for j in xrange(len(inx)):
            		cv2.circle(frame, (inx[j],altura), 2, (0,0,255), -1)
            		cv2.circle(frame, (anchura/2,altura), 2, (255,255,255), -1)
            		centers.append((inx[j],altura))

    	centers = np.flip(centers, 0)
    	#for i in xrange(0, len(centers)-3, 2):
        	#cv2.line(frame,((centers[i][0]-centers[i+1][0])/2+centers[i+1][0], centers[i][1]),((centers[i+2][0]-centers[i+3][0])/2+centers[i+3][0], centers[i+2][1]),(255,0,0),2)

    # For instance, in this example you can enable the Canny edge function above.
    # You will see that the frame rate drops to ~35fps and video playback is erratic.
    # If you then set fps = 30 at the beginning of the script, there will be enough cycle time between frames to provide accurate video.

    # One optimization could be to work with a decimated (downscaled) version of the image: deci = frame[::2, ::2]

    	frames.append(frame) # save the frame (for the demo)
    #del frame # free the allocated memory
    	N_frames += 1
    	if N_frames > max_frames: break

end_time = time.time()

cameraProcess.terminate() # stop the camera

elapsed_seconds = end_time-start_time
print("Done! Result: "+str(N_frames/elapsed_seconds)+" fps")


print("Writing frames to disk...")
out = cv2.VideoWriter("drive_test.avi", cv2.cv.CV_FOURCC(*"MJPG"), 30, (w,h))
for n in range(N_frames):
    #cv2.imwrite("frame"+str(n)+".png", frames[n]) # save frame as a PNG image
    #frame_rgb = cv2.cvtColor(frames[n],cv2.COLOR_GRAY2RGB) # video codec requires RGB image
    out.write(frames[n])
out.release()

#print("Display frames with OpenCV...")
#for frame in frames:
    #cv2.imshow("Slow Motion", frame)
    #cv2.waitKey(1) # request maximum refresh rate

cv2.destroyAllWindows()
