import json
from urllib.parse import urlencode
import webbrowser
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import requests


def get_artist_albums(token, artist_id):
    id = artist_id

    url = "https://api.spotify.com/v1/artists/" + id + "/albums?market=CA&limit=20&include_groups=album"

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
        "time_range": "medium_term"
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
    

def populate_albums(token):
    t = open('topArtists.json')
    tData = json.load(t)

    dict = {}
    count = 0
    for x in tData:
        iDict = get_artist_albums(token, x["id"])
        dict[count] = iDict
        count += 1

    r = json.dumps(dict, indent = 2)
    with open("albums.json", "w") as outfile:
        outfile.write(r)

def compute_result():
    a = open('albums.json')
    aData = json.load(a)

    t = open('topTracks.json')
    tData = json.load(t)

    d = {}

    for x in aData:
        for y in aData[x]["items"]:
            if (y["id"] in d):
                d[y["id"]] += 1
            else:
                d[y["id"]] = 1
    
    for x in tData:
        if (x["album"]["id"] in d):
            d[x["album"]["id"]] += 5
        else: 
            d[x["album"]["id"]] = 5

    s = sorted(d.items(), key=lambda x:x[1], reverse=True)
    m = dict(s)

    r = json.dumps(m, indent = 2)
    with open("result.json", "w") as outfile:
        outfile.write(r)



def get_recommended_albums():
    t = open("result.json")
    tData = json.load(t)

    dict = {}
    i = 0
    for x in tData:
        dict[i] = "https://open.spotify.com/album/" + x
        i += 1
        if (i == 10):
            break
    
    r = json.dumps(dict, indent = 2) 
    with open("albumlinks.json", "w") as outfile:
        outfile.write(r)

def open_albums():
    t = open('albumlinks.json')
    tData = json.load(t)

    for x in tData:
        webbrowser.open(tData[x])
