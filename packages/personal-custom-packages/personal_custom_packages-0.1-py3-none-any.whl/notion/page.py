import requests
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv('api_key')

headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }

children = []

# Define the data payload with the children list
data = {
    'children': children
}



def extract_all_blocks_from_page(page_id):
    response = requests.get(f'https://api.notion.com/v1/blocks/{page_id}/children?', headers=headers)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data: {response.text}")

def extract_core_data_from_all_blocks(results):
    core_data = []
    for i in results:
        entering_stack = i[i["type"]]["rich_text"]
        if len(entering_stack) >= 1:
            
            data = entering_stack[0]["plain_text"]
            core_data.append(data)
    return core_data

# Block number means the imaginary index (start from 1 to the last block)
def extract_text_from_specific_block_number(core_data,block_number):
    for index,text in enumerate(core_data):
        if index+1 == block_number:
            return text
        

def extract_id_from_database_page_url(url):
    arr = url.split("/")
    id = arr[3].split("?")[0].split("-")[4]
    return id
    
extract_id_from_database_page_url("https://www.notion.so/usefulness-of-function-utility-e3be345283334d7da007b677502eccad?pvs=4")

# def extract_block_data(page_id):
#     if page_id === 