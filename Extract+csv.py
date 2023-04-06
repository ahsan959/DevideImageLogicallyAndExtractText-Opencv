import cv2
import pytesseract
import csv

# Path to input image
image_path = 'img1.jpeg'

# Read image using OpenCV
image = cv2.imread(image_path)

# Divide the image into 4 parts (top_left, top_right, bottom_left, bottom_right)
height, width, _ = image.shape
top_left = image[0:height//2, 0:width//2]
top_right = image[0:height//2, width//2:width]
bottom_left = image[height//2:height, 0:width//2]
bottom_right = image[height//2:height, width//2:width]

# Divide bottom_left image into top and bottom parts
bottom_left_height, bottom_left_width, _ = bottom_left.shape
bottom_left_top = bottom_left[0:bottom_left_height//2, :]
bottom_left_bottom = bottom_left[bottom_left_height//2:bottom_left_height, :]

# Extract text from top part of bottom_left image using Tesseract OCR
bottom_left_top_text = pytesseract.image_to_string(bottom_left_top)

# Save extracted text to CSV file
with open('newfile.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Extracted Text'])
    writer.writerow([bottom_left_top_text])

# Save images with proper names
cv2.imwrite('top_left.jpg', top_left)
cv2.imwrite('top_right.jpg', top_right)
cv2.imwrite('bottom_left.jpg', bottom_left)
cv2.imwrite('bottom_right.jpg', bottom_right)
cv2.imwrite('bottom_left_top.jpg', bottom_left_top)
cv2.imwrite('bottom_left_bottom.jpg', bottom_left_bottom)
