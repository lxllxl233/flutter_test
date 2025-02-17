import requests

def send(message):
    from frame.core.frame_config import ConfigManager
    url = ConfigManager.get('REMOTE_URL')+'/send'
    response = requests.post(url, json={
        "message": message
    })
    print(response.status_code)