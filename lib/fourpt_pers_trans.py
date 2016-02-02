# This file has functions necessary to perform four point perspective transform
# Functions available:
#	pers_transform
#	ord_arr_pts

# Get the needed packages
# 	numpy for numerical processing
# 	cv2 for OpenCV Python bindings
import numpy as np
import cv2


def pers_transform(img, points):
	# Get the points in order and extract them separately
	ordarr = ord_arr_pts(points)
	(tl, tr, br, bl) = ordarr

	# Derive new image width, given by the maximum of distance
	# between bottom-right and bottom-left or top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxwdth = max(int(widthA), int(widthB))

	# Derive new image height, given by the maximum of distance
	# between top-right and bottom-right or top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxhght = max(int(heightA), int(heightB))

	# With derived image dimensions, form an ordered array of 
	# new points to get top-down view of the input image
	newpts = np.array([
		[0, 0],
		[maxwdth - 1, 0],
		[maxwdth - 1, maxhght - 1],
		[0, maxhght - 1]], dtype = "float32")

	# Set up perspective transform matrix, apply warping and return the result
	mat = cv2.getPerspectiveTransform(ordarr, newpts)

	warped = cv2.warpPerspective(img, mat, (maxwdth, maxhght))
	return warped

def ord_arr_pts(points):
	# Set up an ordered array of coordinates 
	# Top-left coordinate goes first in the list, second is top-right
	# followed by bottom-right and then bottom-left
	ordarr = np.zeros((4, 2), dtype = "float32")

	# Calculate the sum and difference between point coordinates
	# Bottom-left point will have the smallest sum and top-right will have the largest
	# Bottom-right point will have the smallest difference and top-left will have the largest
	psum = points.sum(axis = 1)
	ordarr[0] = points[np.argmin(psum)]
	ordarr[2] = points[np.argmax(psum)]

	pdiff = np.diff(points, axis = 1)
	ordarr[1] = points[np.argmin(pdiff)]
	ordarr[3] = points[np.argmax(pdiff)]

	# return the ordered coordinates
	return ordarr
