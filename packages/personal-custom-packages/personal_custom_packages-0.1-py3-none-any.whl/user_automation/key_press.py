from data_extractor import log_function_usage
import pyautogui
import subprocess

class mouse_movement:
    def __init__(self):
        log_function_usage('__init__-user_automation-key_press.py')
        self.current_x_position = None
        self.current_y_position = None
        self.current_position()

    def set_position(self,x,y):
        log_function_usage('set_position-user_automation-key_press.py')
        self.current_x_position = x
        self.current_y_position = y
        pyautogui.moveTo(x,y)

    def show_current_position(self):
        log_function_usage('show_current_position-user_automation-key_press.py')
        x, y = pyautogui.position()
        return {"x": x, "y": y}

    def current_position(self):
        log_function_usage('current_position-user_automation-key_press.py')
        x, y = pyautogui.position()
        self.current_x_position = x
        self.current_y_position = y
        print(self.current_x_position,self.current_y_position)

    def get_current_cursor_coordinate(self):
        log_function_usage('get_current_cursor_coordinate-user_automation-key_press.py')
        return f"x: {self.current_x_position}, y: {self.current_y_position}"

    def move_left(self,units):
        log_function_usage('move_left-user_automation-key_press.py')
        self.current_x_position -= units
        pyautogui.moveTo(self.current_x_position,self.current_y_position)

    def move_right(self,units):
        log_function_usage('move_right-user_automation-key_press.py')
        self.current_x_position += units
        pyautogui.moveTo(self.current_x_position,self.current_y_position)
        

    def move_up(self,units):
        log_function_usage('move_up-user_automation-key_press.py')
        self.current_y_position -= units

    def move_down(self,units):
        log_function_usage('move_down-user_automation-key_press.py')
        self.current_x_position += units

    def next_app(self,number):
        log_function_usage('next_app-user_automation-key_press.py')
        pyautogui.keyDown("command")
        for i in range(number):
            pyautogui.press("tab")
        pyautogui.keyUp("command")

