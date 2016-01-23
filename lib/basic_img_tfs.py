# This file has functions for general basic image transformations
# Functions available:
#	resize_img
#	rotate_img
#	translate_img

# Get the needed packages
# 	numpy for numerical processing
# 	cv2 for OpenCV Python bindings
import numpy as np
import cv2

def resize_img(img, width = None, height = None, inter = cv2.INTER_AREA):
	# Set up the image dimensions to be resized and get size of the image
	dim = None
	(hght, wdth) = img.shape[:2]

	# Return original image if input dimensions are None, else calculate new dimensions
	if width is None and height is None:
		return img

	if width is None:
		# Derive height ratio to construct new dimensions
		ratio = height / float(hght)
		newdim = (int(wdth * ratio), height)
	else:
		# Derive width ratio to construct new dimensions
		ratio = width / float(wdth)
		newdim = (width, int(hght * ratio))

	# Resize and return image
	resized = cv2.resize(img, newdim, interpolation = inter)
	return resized

def rotate_img(img, angle, center = None, scale = 1.0):
	# Get the image dimensions and calculate the center
	(hght, wdth) = img.shape[:2]
	if center is None:
		center = (wdth / 2, hght / 2)

	# Set up rotation matrix M, perform rotation and return the rotated image
	mat = cv2.getRotationMatrix2D(center, angle, scale)

	rotated = cv2.warpAffine(img, mat, (wdth, hght))
	return rotated

def translate_img(img, xcoor, ycoor):
	# Set up translation matrix M, perform translation and return the translated image
	mat = np.float32([[1, 0, xcoor], [0, 1, ycoor]])

	shifted = cv2.warpAffine(img, mat, (img.shape[1], img.shape[0]))
	return shifted
