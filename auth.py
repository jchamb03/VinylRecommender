import json
from urllib.parse import urlencode
import webbrowser
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import requests



load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
auth_code = os.getenv("AUTH_CODE")


def get_user_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")


    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + encoded_credentials,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code" : auth_code,
        "redirect_uri": "http://localhost:7777/callback"
    }


    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    r = json.dumps(json_result, indent = 2)
    with open("auth_data.json", "w") as outfile:
        outfile.write(r)
    

def get_basic_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")


    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + encoded_credentials,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    result = post(url,headers = headers, data = data)
    json_result = json.loads(result.content)
    r = json.dumps(json_result, indent = 2)
    with open("data.json", "w") as outfile:
        outfile.write(r)


def authorize_user_access():
    auth_headers = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": "http://localhost:7777/callback",
    "scope": "user-top-read user-library-read user-read-private",
    }
    result = webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))



def get_auth_header(token):
    return {"Authorization": "Bearer " + token}




def refresh_auth_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")

    f = open('auth_data.json')
    data = json.load(f)

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + encoded_credentials,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": data["refresh_token"],
    }

    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    r = json.dumps(json_result, indent = 2)
    with open("auth_data.json", "w") as outfile:
        outfile.write(r)

