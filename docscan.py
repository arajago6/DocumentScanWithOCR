# This file is the driver script that does everything from start to end

# Get the needed packages
#	image_file_to_string for invoking tesseract from python script
#	pers_transform for getting top-down view on the input image	
#	resize_img for applying basic resizing transformation to image
#	threshold_adaptive to apply better dynamic thresholding to processed input image 
# 	numpy for numerical processing
# 	cv2 for OpenCV Python bindings
from pytesser.pytesser import image_file_to_string
from lib.fourpt_pers_trans import pers_transform
from lib.basic_img_tfs import resize_img
from skimage.filters import threshold_adaptive
import numpy as np
import argparse
import cv2

# Build the argument parser and split the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to image that is to be converted to text")
args = vars(ap.parse_args())

print ("*** Starting DocScan v1.0 ***");

# Read the image, derive the ratio of the old height
# to the new height, make a copy of it and resize the image
image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
orig = image.copy()
image = resize_img(image, height = 500)

# Display the resized original image
cv2.imshow("DocScan V1.0 - Press any key to continue", image)

# Apply grayscaling, smoothing and then detect edges
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)

# Display the edge detected image
print "Edges detected already - Press any key to view edge image"
cv2.waitKey(0)
cv2.imshow("DocScan V1.0 - Press any key to continue", edged)

# Find contours in the edge image, keeping only the
# first five largest ones and set up the screen contour
(_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

# Iterate over the contours, approximate them and if a contour 
# has 4 points, take it as the screen
for c in cnts:
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

	if len(approx) == 4:
		screenCnt = approx
		break

# Draw the contour (outline) of the piece of paper on image
cv2.drawContours(image, [screenCnt], -1, (255, 255, 0), 2)

# Display the resized original image with contour
print "Contour detected already - Press any key to view the contour"
cv2.waitKey(0)
cv2.imshow("DocScan V1.0 - Press any key to continue", image)

# Apply perspective transform to obtain a top-down
# view of the original image
print "Perspective transform can be applied - Press any key to start transform"
cv2.waitKey(0)
print "Please wait while perspective transform is being applied..."
warped = pers_transform(orig, screenCnt.reshape(4, 2) * ratio)

# Grayscale the warped image, then apply adaptive thresholding on it to binarize
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
warped = threshold_adaptive(warped, 250, offset = 10)
warped = warped.astype("uint8") * 255

# Can smooth the warped image if that seems to give better result
warped = cv2.GaussianBlur(warped,(1,1),0)

# Display the resultant image after perspective transform
print "Perspective transform applied successfully. Press any key to start text extraction"
cv2.imshow("DocScan V1.0 - Press any key to continue", resize_img(warped, height = 500))
cv2.waitKey(0)

# Save the resulatant image and call tesseract with the saved image file name 
cv2.imwrite("result/out.tiff",warped)
print "Starting text extraction with Tesseract..."
text = image_file_to_string("result/out.tiff")
f = open("result/out.txt","w")
f.write(text)
print "Text extraction was successful. Text saved to out.txt in result folder"
print "*** Thanks for using DocScan V1.0! See you again, soon! ***"
cv2.destroyAllWindows()
