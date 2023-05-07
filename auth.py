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

f = open('data.json')
data = json.load(f)

token = data["access_token"]

def get_token():
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
    with open("data.json", "w") as outfile:
        outfile.write(r)
    
    token = json_result["access_token"]
    return token

def authorize_user_access():
    auth_headers = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": "http://localhost:7777/callback",
    "scope": "user-top-read user-library-read"
    }
    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def get_top_tracks(token):
    url = "https://api.spotify.com/v1/me/top/tracks"
    user_headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }
    user_params = {
        "limit": 50
    }
    user_tracks_response = get(url,params = user_params, headers = user_headers)
    json_result = json.loads(user_tracks_response.content)["items"]
    r = json.dumps(json_result, indent = 2)
    with open("topTracks.json", "w") as outfile:
        outfile.write(r)
