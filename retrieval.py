import json
from urllib.parse import urlencode
import webbrowser
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import requests

from auth import get_auth_header


t = open('topTracks.json')
tData = json.load(t)
for i in range (0,49):
    print("Song: " + tData[i]["name"] + "\n" + "Artist: " + tData[i]["album"]["artists"][0]["name"])
    print("\n")
    

def search_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"

    headers = get_auth_header(token)
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
    
def get_artist_top_tracks(token):
    url = "https://api.spotify.com/v1/artists/3WrFJ7ztbogyGnTHbHJFl2/top-tracks?market=CA"

    headers = get_auth_header(token)

    result = get(url, headers = headers)
    json_result = json.loads(result.content)
    r = json.dumps(json_result)
    with open("data.json", "w") as outfile:
        outfile.write(r)
    return json_result