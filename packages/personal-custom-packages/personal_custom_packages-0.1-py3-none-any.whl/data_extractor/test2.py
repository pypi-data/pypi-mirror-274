import pyautogui
from PIL import Image
# import datetime

# # Create a datetime object representing April 27, 2024, 12:00:00 PM
# dt = datetime.datetime(2024, 4, 27, 12, 0, 0)

# # Get the timestamp for the specified datetime object
# timestamp = dt.timestamp()

# print("Timestamp:", timestamp)
screen_width, screen_height = pyautogui.size()

# Set the coordinates of the region to capture (left, top, width, height)
x, y, width, height = 405, 194, 474, 21

screenshot = pyautogui.screenshot()

cropped_image = screenshot.crop((x, y, x + width, y + height))

cropped_image.save('cropped_image.png')

cropped_image.show()
