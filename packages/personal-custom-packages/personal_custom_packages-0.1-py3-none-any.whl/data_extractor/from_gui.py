import pyautogui

# import time
# from PIL import ImageGrab
# from PIL import Image

def screen_shot_section(top_left_x,top_left_y,width,height):
    screenshot = pyautogui.screenshot(region=(top_left_x, top_left_y, width, height))
    return screenshot



# screen_shot_section()


# pyautogui.keyDown("command")
# pyautogui.press("tab")
# time.sleep(0.5)
# pyautogui.keyUp("command")
# pyautogui.press("enter")
# pyautogui.hotkey('command', 'enter')

# ONE: GET THE POSITION OF YOUR MOUSE
# x, y = pyautogui.position()

# with open("capture.txt", "a") as f:
#     # Write a single line to the file
#     f.write(f"x:{x},y:{y}\n")
    

# counter = 0

# while counter < 10:
#     time.sleep(1)
#     pyautogui.move(100, 0)  # Move 100 pixels to the right horizontally
#     counter+=1

# print("COMPLETED!!!")


# print(x,y)

# left
# x: 405 -> 405
# y: 194 -> 215
# bottom right
# x: 879 -> 879
# y: 215 -> 194




# Get the screen resolution
# screen_width, screen_height = pyautogui.size()

# # Set the coordinates of the region to capture (left, top, width, height)
# x, y, width, height = 405, 194, 474, 21

# screenshot = pyautogui.screenshot()

# cropped_image = screenshot.crop((x, y, x + width, y + height))

# cropped_image.save('cropped_image.png')

# cropped_image.show()