import cv2
import pyautogui
import numpy as np

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    # Capture the screen image
    screen = pyautogui.screenshot()

    # Convert the screen image to a format compatible with OpenCV
    screen_np = np.array



