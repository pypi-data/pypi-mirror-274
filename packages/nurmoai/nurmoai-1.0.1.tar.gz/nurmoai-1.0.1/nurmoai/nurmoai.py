import os
import requests

class NurmoAI:
    def __init__(self, api_key=None):
        self.api_key = api_key if api_key is not None else os.environ.get('NURMO_KEY')
        self.base_url = 'https://api.nurmo.app/chat/completions'

    def create_completion(self, messages, model, character=None):
        headers = {'Authorization': f'Bearer {self.api_key}'}
        if character is None:
            raise ValueError("Please provide a character name.")

        data = {'model': model, 'messages': messages, character: character}

        response = requests.post(self.base_url, json=data, headers=headers)
        response_text = response.text

        try:
            response_data = response.json()
            if 'error' in response_data:
                if response_data['error'] == "Unknown model":
                    raise Exception(f"Unknown model named {model}")
                else:
                    raise Exception(response_data['error'])
        except:
            pass

        return response_text
