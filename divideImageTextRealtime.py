# write a program opencv divide image Logically and save images and use only Bottom Left image again divide this image into two parts top and bottom and again divide top and bottom and Extract Text from top and save in csv file in using Live Camera

import cv2
import numpy as np
import pytesseract
import csv
import re

# Initialize the camera
camera = cv2.VideoCapture(0)

# Initialize the CSV file
csv_file = open('output.csv', mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Text'])

while True:
    # Capture the frame from the camera
    ret, frame = camera.read()

    # Divide the frame logically into four parts
    height, width = frame.shape[:2]
    half_height = height // 2
    half_width = width // 2
    top_left = frame[0:half_height, 0:half_width]
    top_right = frame[0:half_height, half_width:width]
    bottom_left = frame[half_height:height, 0:half_width]
    bottom_right = frame[half_height:height, half_width:width]

    # Divide the bottom left image into top and bottom parts
    bl_height, bl_width = bottom_left.shape[:2]
    bl_half_height = bl_height // 2
    bl_top = bottom_left[0:bl_half_height, 0:bl_width]
    bl_bottom = bottom_left[bl_half_height:bl_height, 0:bl_width]

    # Convert the top portion of the bottom left image to grayscale
    gray = cv2.cvtColor(bl_top, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to the grayscale image
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Remove noise from the image using morphological operations
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)

    # Apply OCR to the processed image and remove commas and other special characters from the extracted text
    bl_top_text = pytesseract.image_to_string(closing)
    bl_top_text = re.sub('[^A-Za-z0-9]+', '', bl_top_text)

    # Save the text to the CSV file if it is not empty
    if bl_top_text:
        csv_writer.writerow([bl_top_text])

    # Display the processed frame
    cv2.imshow('Processed Frame', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the CSV file
camera.release()
csv_file.close()

# Destroy all windows
cv2.destroyAllWindows()

