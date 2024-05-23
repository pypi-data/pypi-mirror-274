# api/__init__.py

import requests
import json

def call_gemma_api(user_query, llm_new_tokens, access_token):
    url = 'https://ai.platform.qubrid.com/gemma'
    headers = {
        'Content-Type': 'application/json',
        'x-access-token': access_token
    }
    data = {
        'user_query': user_query,
        'llm_new_tokens': llm_new_tokens
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()
