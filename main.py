import json
import auth
import retrieval



#  Must do authentication first, must have authentication code available in .env
#  Can either use user-authorized token, which has some special stuff to do, or for searching basic public data can use a basic token at any time


# Get authorization tokens, put them in json files. 
# auth.get_user_token()
# auth.get_basic_token()

# Retrieve the tokens from json file
t = open("auth_data.json")
auth_token = json.load(t)["access_token"]

d = open("data.json")
basic_token = json.load(d)["access_token"]

# Retrieve user data
retrieval.get_top_artists(auth_token)
retrieval.get_top_tracks(auth_token)
# Get albums from top artists
retrieval.populate_albums(basic_token)

# Calculate recommendation scores for albums
retrieval.compute_result()
# populate the links for albums
retrieval.get_recommended_albums()
# open the links to albums in web browser
retrieval.open_albums()