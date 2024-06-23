import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging
logger = logging.getLogger(__name__)
# Set up authentication flow
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='be97332ad2c1491f99646b7a22104898',
                                               client_secret='4b38893cb9a94ecfbea77d64b4760379',
                                               redirect_uri='http://localhost:8888/callback',
                                               scope='playlist-read-private'))
username = input("Enter your Spotify Username: ")
user_playlists = sp.user_playlists(username)


for playlist in user_playlists['items']:
    print(playlist['name'])

