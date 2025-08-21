import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

# Load environment variables from .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Define the scope: adjust based on what data you need
scope = ["user-library-read","user-top-read"]
  # allows reading your saved tracks

# Authenticate with Spotify using OAuth
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI")
    )
)

# Get the user's saved tracks
print("Fetching your saved tracks...")
results = sp.current_user_top_tracks(limit=50, offset=0, time_range='medium_term')

# pprint.pp(results['items'][0]['album']['name'])
# pprint.pp(results['items'][0]['name'])
# # Display saved tracks
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(f"{idx+1}. {track['artists'][0]['name']} - {track['name']}")

top_songs = ""

for item in results['items']:
    track = item['album']
    # print(f"Name: {track['name']}")
    top_songs += f"{item['name']} - "
    for artists in track['artists']:
        top_songs += f"{artists['name']}, "
        # pprint.pp(f"Artist: {artists['name']}")

    top_songs += "\n"
    
    # pprint.pp(f"Artist: {track['artists']}")
print("Top songs:")
print(top_songs)
