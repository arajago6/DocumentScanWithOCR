# Document Scanner with OCR

Can detect documents in trivial images, process it and extract text from it.
Uses OpenCV for document processing and Tesseract for optical text recognition.

Usage: 
python docscan.py -i data/Sample1.jpg

Roadmap:
Release standalone Linux desktop version and smartphone versions of this project.
Improve the accuracy of the project.
	Possible areas:
		Automate some parts of Tesseract training module for easier training.
		Use different levels of smoothing, compare text outputs and merge them so as to get high accuracy.
		Extensively learn Tesseract's methods to modify them for greater accuracy.

