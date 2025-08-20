import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# print("Spotify client initialized ✅")

# Load environment variables from .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Define the scope: adjust based on what data you need
scope = "user-library-read"  # allows reading your saved tracks

# Authenticate with Spotify using OAuth
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        open_browser=True
    )
)

# Get the user's saved tracks
results = sp.current_user_saved_tracks(limit=10)

# Display saved tracks
for idx, item in enumerate(results['items']):
    track = item['track']
    print(f"{idx+1}. {track['artists'][0]['name']} - {track['name']}")

# print("Spotify client initialized ✅")
print("Client ID:", os.getenv("SPOTIPY_CLIENT_ID"))

# import spotipy
# from spotipy.oauth2 import SpotifyOAuth

# scope = "user-library-read"

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])
