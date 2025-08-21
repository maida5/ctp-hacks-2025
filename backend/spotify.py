import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# load environment variables from .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# define the scope: adjust based on what data you need
scope = "user-library-read" # allows reading your saved tracks

# authenticate with spotify using OAuth
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI")
    )
)

# get user's saved tracks
results = sp.current_user_saved_tracks(limit=10)

# display saved tracks
for idx, item in enumerate(results['items']):
    track = item['track']
    print(f"{idx+1}. {track['artists'][0]['name']} - {track['name']}")
