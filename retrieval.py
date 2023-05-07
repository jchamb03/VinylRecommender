import json
from urllib.parse import urlencode
import webbrowser
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import requests


f = open('data.json')
data = json.load(f)

token = data["access_token"]

t = open('topTracks.json')
tData = json.load(t)
# for i in range (0,49):
#     print("Song: " + tData[i]["name"] + "\n" + "Artist: " + tData[i]["album"]["artists"][0]["name"])
#     print("\n")
    

def search_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"

    headers = {"Authorization": "Bearer " + token}
    query = f"q={artist_name}&type=artist&limit=1"

    query_url = url + "?" + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No Artist Found")
        return None
    return json_result[0]   

def get_artist_id(token, artist_name):
    result = search_artist(token, artist_name)
    return result['id']
    
def get_artist_top_tracks(token, artist_name):
    id = get_artist_id(token,artist_name)

    url = "https://api.spotify.com/v1/artists/" + id + "/top-tracks?market=CA"

    headers = {"Authorization": "Bearer " + token}

    result = get(url, headers = headers)
    json_result = json.loads(result.content)
    return json_result

