
import requests
import json

### Example payload for data dict
#    data = {
#        'category': category,
#        'sub-category': sub_category,
#        'term': term
#    }
###


def completeChat(prompt, model, data):
    url = "http://localhost:11434/api/generate"
    call = {
        "model": model,
        "prompt": prompt,
        "stream":False
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(call))
    return response.json()
    
