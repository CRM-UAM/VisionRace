import numpy as np

def SlicePart(image, slices, i):
	height, width  = image.shape[:2]
	sl = int(height/slices);
	part = sl*(i-1)
	crop_img = image[part:part+sl, 0:width]
	
	return crop_img

