import requests
import json

def postData(url,payload):
    r = requests.post(url,data=payload)
    return json.loads(r.text)

def token_load(config):
    payload = { 'token' : config['accessToken'] }
    url = 'https://slack.com/api/auth.test'
    data = postData(url,payload)
    if data["ok"] == True:
        return None

    payload = { 'refresh_token': config['refreshToken'] }
    url = 'https://slack.com/api/tooling.tokens.rotate'
    data = postData(url,payload)
    if data["ok"] == True:
        config['accessToken'] = data['token']
        config['refreshToken'] = data['refresh_token']
        return config
    raise Exception('Slack Token Fail')

def auth_load(token):
    payload = { 'token' : token }
    url = 'https://slack.com/api/auth.test'
    data = postData(url,payload)
    if data["ok"] == True:
        return data
    return None
    
