import cv2
import pytesseract
import csv
import numpy as np

# Load the image
img = cv2.imread('img1.jpeg')

# Divide the image logically
h, w = img.shape[:2]
sub_img_w = w // 2
sub_img_h = h // 2
sub_imgs = [
    img[:sub_img_h, :sub_img_w],
    img[:sub_img_h, sub_img_w:],
    img[sub_img_h:, :sub_img_w],
    img[sub_img_h:, sub_img_w:]
]

# Extract the bottom-left sub-image
bottom_left = sub_imgs[2]

# Divide the bottom-left sub-image into two parts
bl_h, bl_w = bottom_left.shape[:2]
bl_sub_h = bl_h // 2
bl_top = bottom_left[:bl_sub_h, :]
bl_bottom = bottom_left[bl_sub_h:, :]

# Divide the top sub-image again into two parts
bl_top_h, bl_top_w = bl_top.shape[:2]
bl_top_sub_h = bl_top_h // 2
bl_top_top = bl_top[:bl_top_sub_h, :]
bl_top_bottom = bl_top[bl_top_sub_h:, :]

# Extract text from the top sub-sub-image
bl_top_top_text = pytesseract.image_to_string(bl_top_top)

# Save extracted text to CSV file
with open('newfile.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Extracted Text'])
    writer.writerow([bl_top_top_text])
# Print the extracted text
print(bl_top_top_text)
