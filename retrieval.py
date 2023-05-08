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

def get_top_tracks(token):
    url = "https://api.spotify.com/v1/me/top/tracks"
    user_headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }
    user_params = {
        "limit": 50,
        "time_range": "long_term"
    }
    user_tracks_response = get(url,params = user_params, headers = user_headers)
    json_result = json.loads(user_tracks_response.content)["items"]
    r = json.dumps(json_result, indent = 2)
    with open("topTracks.json", "w") as outfile:
        outfile.write(r)


def get_top_artists(token):
    url = "https://api.spotify.com/v1/me/top/artists"
    user_headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }
    user_params = {
        "limit": 20
    }
    user_tracks_response = get(url,params = user_params, headers = user_headers)
    json_result = json.loads(user_tracks_response.content)["items"]
    r = json.dumps(json_result, indent = 2)
    with open("topArtists.json", "w") as outfile:
        outfile.write(r)

def print_tracks():
    t = open('topTracks.json')
    tData = json.load(t)
    for i in range (0,49):
        print("Song: " + tData[i]["name"] + "\n" + "Artist: " + tData[i]["album"]["artists"][0]["name"])
        print("\n")
    


