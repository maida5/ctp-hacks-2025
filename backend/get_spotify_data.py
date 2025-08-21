import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

def set_up_spotify_client():
    # Load environment variables from .env
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

    # Define the scope: adjust based on what data you need
    scope = ["user-library-read","user-top-read", "playlist-modify-public"]
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
    return sp


def get_spotify_top_songs():
    sp = set_up_spotify_client()

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
    return top_songs

def return_spotify_songs():
    sp = set_up_spotify_client()

    artist = "Duran Duran"
    artist = artist.replace(" ", "%20")
    song = "Union of the Snake"
    song = song.replace(" ", "%20")
    q = f"{artist}%20{song}"
    track = sp.search(q=q, type='track', limit=1)
    # print(track)
    return track['tracks']['items'][0]['uri']

def create_playlist():
    sp = set_up_spotify_client()
    user_id = sp.current_user()['id']
    playlist_name = "My Playlist"
    playlist_description = "A playlist created by my app"
    
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True, description=playlist_description)
    print(f"Created playlist: {playlist['name']} with ID: {playlist['id']}")
    return playlist['id']

def add_tracks_to_playlist(playlist_id, track_ids):
    sp = set_up_spotify_client()
    sp.playlist_add_items(playlist_id, track_ids)
    print(f"Added tracks to playlist {playlist_id}")

print(return_spotify_songs())
playlist_id = create_playlist()
song_id = return_spotify_songs()
add_tracks_to_playlist(playlist_id, [song_id])

