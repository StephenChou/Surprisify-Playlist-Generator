import sys
import os
import spotipy
import spotipy.util as util
import random
import requests
# from urllib.parse import urlencode
import base64

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")


def authenticate():
	
	scope = 'user-top-read user-library-read playlist-modify-public'
	username = sys.argv[0]

	# try:
	token = util.prompt_for_user_token(username,
	                               scope,
	                               client_id,
	                               client_secret,
	                               redirect_uri='http://localhost:8080/',
	                               )
	if token:
		return token
	else:
		return False

def get_obscure_artist(artist_id, levels, spotifyObject):

    rnd_artist = random.randint(0, 11)
    
    if (levels == 1):
        return artist_id

    tempid = spotifyObject.artist_related_artists(artist_id)['artists'][rnd_artist]['id']
    finalid = get_obscure_artist(tempid, levels -1, spotifyObject)
    return finalid

def generate(token, levels):

	spotifyObject = spotipy.Spotify(auth=token)

	user_id = str(spotifyObject.current_user()['id'])
	first_name = spotifyObject.current_user()['display_name'].split()[0]

	# Get user top artists
	user_top_artists = spotifyObject.current_user_top_artists(limit=5,time_range='medium_term')

	# Put top artists in dictionary
	artist_ids = []
	for artist in user_top_artists['items']:
	    artist_ids.append(artist['id'])

	# Try and get obscure artists by going deep into related artists
	related_artist_ids = []
	for i in artist_ids:
		id = get_obscure_artist(i, levels, spotifyObject)
		while id not in related_artist_ids:
			id = get_obscure_artist(i, levels, spotifyObject)
			related_artist_ids.append(id)

	# Get list of recommended songs and put ID's in a list
	tracks = spotifyObject.recommendations(seed_artists=related_artist_ids, limit=50)
	track_ids = []
	for track in tracks['tracks']:
	    track_ids.append(track['id'])

	# Put recommended songs into playlist
	recommended_playlist = spotifyObject.user_playlist_create(user_id, ("Surprisify playlist for {}".format(first_name)), description=("{} level(s) deep").format(levels))
	recommended_playlist_id = recommended_playlist['id']
	spotifyObject.user_playlist_add_tracks(user_id, recommended_playlist_id, track_ids)



