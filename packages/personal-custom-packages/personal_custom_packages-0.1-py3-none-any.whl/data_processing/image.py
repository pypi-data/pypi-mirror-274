import pytesseract
from PIL import Image
import io

def convert_image_to_bytes(image_data):
    return image_data.toBytes()

def generate_text_data_from_image(image_obj):
    return pytesseract.image_to_string(image_obj)



print("HELLO")