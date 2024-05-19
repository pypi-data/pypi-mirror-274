import subprocess
# from data_extractor import log_function_usage
import pyperclip

def add_text_to_clipboard(text_to_copy):
    pyperclip.copy(text_to_copy)

def display_popup(message):
    # log_function_usage('display_popup-user_automation-key_press.py')
    applescript = f'display notification "{message}" with title "Popup"'
    subprocess.run(['osascript', '-e', applescript])

