# Document Scanner with OCR

To detect documents in trivial images, process them and extract text from them. 
Used OpenCV v3.0 for document processing and Tesseract v3.03 for optical text recognition

Usage: 
python docscan.py -i data/Sample1.jpg

Roadmap:
- Release standalone Linux desktop version and smartphone versions of this project.
- Improve the accuracy of the project.
	- Possible areas for imrpovement:
		- Automate some parts of Tesseract training module for easier training.
		- Use different levels of smoothing on Tesseract input, compare text outputs and merge them so as to get high accuracy.
		- Extensively learn Tesseract's methods to try and modify them for greater accuracy.
