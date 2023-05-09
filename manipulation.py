import json
import auth
import retrieval




def populate_tracks():
    trackList = [dict() for x in range(50)]
    t = open('topTracks.json')
    tData = json.load(t)
    for i in range (0,49):
        trackList[i] = {
            "artist_name": tData[i]["album"]["artists"][0]["name"],
            "artist_ID": tData[i]["album"]["artists"][0]["id"],
            "album_name": tData[i]["album"]["name"],
            "album_ID": tData[i]["album"]["id"],
            "song_name": tData[i]["name"],
            "song_ID": tData[i]["id"]
        }

    return trackList


def populate_artists():
    artistList = [dict() for x in range(50)]
    t = open('topArtists.json')
    aData = json.load(t)
    for i in range (0,49):
        artistList[i] = {
            "artist_name": aData[i]["name"],
            "artist_id": aData[i]["id"]
        }
    
    return artistList