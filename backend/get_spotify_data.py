import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint
from typing import List, Optional


def set_up_spotify_client():
    # Load environment variables from .env
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

    # Define the scope: adjust based on what data you need
    scope = ["user-library-read","user-top-read", "playlist-modify-public", "playlist-modify-private"]
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

def _quote(term):
    term = (term or "").strip().replace('"', r'\"')
    return f'"{term}"' if " " in term else term




def get_spotify_top_songs(limit=50, time_range="medium_term", sp=None):
    sp = sp or set_up_spotify_client()
    results = sp.current_user_top_tracks(limit=limit, offset=0, time_range=time_range)
    items = results.get("items", []) or []
    lines = []
    for t in items:
        artists = ", ".join(a["name"] for a in t.get("artists", []))
        lines.append(f"{t['name']} – {artists}")
    return lines
def return_spotify_songs(artist, song, market="US" , limit_per_query=3, sp=None):
    sp = sp or set_up_spotify_client()
#input artist and song name as a parameter 
#needs input from gemini to get uri ID, but currently only in testing mode. need to call multiple times, only gets one song at a time 
    queries = [
        f'track:{_quote(song)} artist:{_quote(artist)}',
        f'{_quote(song)} {_quote(artist)}',
        f'track:{_quote(song)}',
    ]
    best = None
    for q in queries:
        res = sp.search(q=q, type="track", market=market, limit=max(1, min(limit_per_query, 50)))
        items = (res.get("tracks") or {}).get("items") or []
        if not items:
            continue
        items.sort(key=lambda t: (0 if t["name"].lower() == song.lower() else 1, -t.get("popularity", 0)))
        best = items[0]
        if best and best["name"].lower() == song.lower():
            break
    return best["uri"] if best else None

def create_playlist(name = "My Playlist", description="A playlist created by my app", public=True, sp=None):
    sp = sp or set_up_spotify_client()
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user=user_id, name=name, public=public, description=description)
    return playlist["id"]

def add_tracks_to_playlist(playlist_id, track_ids):
    sp = sp or set_up_spotify_client()
    sp.playlist_add_items(playlist_id, track_ids)
    #print(f"Added tracks to playlist {playlist_id}")


def add_tracks_batched(playlist_id, track_ids, batch_size=100, sp =None):
    sp = sp or set_up_spotify_client()
    for i in range(0, len(track_ids), batch_size):
        sp.playlist_add_items(playlist_id, track_ids[i:i + batch_size])
