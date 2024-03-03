import os
import requests

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())  


def upload(path): 

    files = [
        ('file', ('file', open(path, 'rb'), 'application/octet-stream'))
    ]

    headers = {
        'x-api-key': os.getenv('GPT_API_TOKEN'),

    }

    Source_id = requests.post('https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files).json()['sourceId']

    return Source_id


def chat(Source_id, message):

    headers = {
        'x-api-key': os.getenv('GPT_API_TOKEN'),
        "Content-Type": "application/json",
    }

    data = {
        "referenceSources": True,
        'sourceId': Source_id,
        'messages': [
            {
                'role': "user",
                'content': message,
            }
        ]
    }

    response = requests.post(
        'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['content']
    else:
        return response.status_code, response.text


