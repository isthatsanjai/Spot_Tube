import os
from urllib.parse import urlencode
import requests
import spotipy
from spotipy import SpotifyOAuth
from pytube import YouTube
import logging


# Function to search for a song on YouTube and return the video ID
def search_youtube(song_title, artist):
    youtube_api_key = 'AIzaSyDRGfYeWNBlf9i0NDWlZcXSKvMmGrMXGI0'
    search_query = f'{song_title} {artist} official lyric video'
    params = {
        'part': 'snippet',
        'q': search_query,
        'key': youtube_api_key,
        'maxResults': 1
    }
    url = f'https://www.googleapis.com/youtube/v3/search?{urlencode(params)}'
    response = requests.get(url)
    data = response.json()
    if 'items' in data:
        items = data['items']
        if items:
            return items[0]['id']['videoId']
    return None


# Set up your Spotify API credentials
os.environ['SPOTIPY_CLIENT_ID'] = 'be97332ad2c1491f99646b7a22104898'
os.environ['SPOTIPY_CLIENT_SECRET'] = '4b38893cb9a94ecfbea77d64b4760379'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback'

# Initialize Spotipy with your credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-read-private"))

# Get user's playlists
playlists = sp.current_user_playlists()

# Print the playlists
for idx, playlist in enumerate(playlists['items']):
    print(f"{idx + 1}. {playlist['name']}")

# Prompt user to select a playlist
playlist_index = int(input("Enter the index of the playlist you want to explore: ")) - 1
selected_playlist_id = playlists['items'][playlist_index]['id']

# Get tracks in the selected playlist
tracks = sp.playlist_items(selected_playlist_id)

# For Downloading YouTube links as Audio files
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def download_video_as_mp3(link):
    try:
        yt = YouTube(link)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path="C:/Users\sanja\Downloads")
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        logger.info(f"Downloaded and converted to MP3: {new_file}")
        return new_file
    except Exception as e:
        logger.error(f"Error downloading the video: {e}")
        return None


list_of_track_links = []
n = 1
# Print track names and YouTube links
print("\nSongs in the playlist with YouTube links:")
for track in tracks['items']:
    track_name = track['track']['name']
    artist = track['track']['artists'][0]['name']
    youtube_video_id = search_youtube(track_name, artist)
    if youtube_video_id:
        youtube_link = f"https://www.youtube.com/watch?v={youtube_video_id}"
        print(f"{n}.{track_name} by {artist}: {youtube_link}")
        list_of_track_links.append(youtube_link)
    else:
        print(f"Could not find YouTube link for {n}.{track_name} by {artist}")
    n += 1
i = int(input("Enter the index of the song you want to download: "))
download_video_as_mp3(list_of_track_links[i-1])
