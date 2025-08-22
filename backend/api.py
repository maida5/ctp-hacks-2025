
from fastapi import FastAPI, UploadFile, File, HTTPException
# import google
from google import genai
from dotenv import load_dotenv
from pathlib import Path 
from google.genai import types
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import os
import requests
from typing import List, Optional  
import re
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from get_spotify_data import (
    set_up_spotify_client,
    return_spotify_songs,     
    add_tracks_to_playlist,   
)

load_dotenv() #Loads backend/ .env
GEMINI_KEY = os.getenv("GEMINI_KEY")
if not GEMINI_KEY:
    raise RuntimeError("Gemini key is missing")

client =genai.Client(api_key=GEMINI_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["https://ctp-hacks-2025-maida5s-projects.vercel.app/","https://ctp-hacks-2025-maida5-maida5s-projects.vercel.app/"],  # Or specify your frontend URL
   allow_origins=[
        "http://localhost:5173", "http://127.0.0.1:5173",
        "http://localhost:3000", "http://127.0.0.1:3000",
        "*" 
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

#parsing
DASHES = r"[-–—]"  

def extract_summary_and_pairs(text: str):
    """
    Returns:
      summary: first two sentences
      pairs:   list of (song, artist) from numbered/bulleted 'Song – Artist' lines
    """
    text = (text or "").strip()

    # first two sentences (., !, ?), allow closing quotes
    m = re.search(r'^\s*(.+?[.!?]["\']?)\s+(.*?[.!?]["\']?)\s*(.*)$', text, flags=re.S)
    if m:
        s1, s2, rest = m.group(1).strip(), m.group(2).strip(), m.group(3)
        summary = f"{s1} {s2}".strip()
    else:
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        if len(lines) >= 2:
            summary = f"{lines[0]} {lines[1]}"
            rest = "\n".join(lines[2:])
        else:
            summary = text
            rest = ""

    # parse Song – Artist lines
    pairs = []
    for raw in rest.splitlines():  # <-- fixed typo
        line = raw.strip()
        if not line:
            continue
        # strip list markers like "1)", "2.", "-", "•"
        line = re.sub(r"^\s*(?:\d+\s*[\).\]]|\-|\*|•|–|—)\s*", "", line)
        parts = re.split(rf"\s*{DASHES}\s*", line, maxsplit=1)
        if len(parts) == 2:
            song, artist = parts[0].strip(" '\""), parts[1].strip(" '\"")
            if song and artist:
                pairs.append((song, artist))

    #  preserve order
    seen, uniq = set(), []
    for s, a in pairs:
        key = (s.lower(), a.lower())
        if key not in seen:
            seen.add(key)
            uniq.append((s, a))
    return summary, uniq

@app.get("/hello")
def root():
    print("Hello World")
    return {"message": "Hello World"}


@app.post("/analyze")
async def analyze_images(
    files: Optional[List[UploadFile]] = File(None),  
    file: Optional[UploadFile] = File(None),          
):
    uploads: List[UploadFile] = []
    if files:
        uploads.extend(files)
    if file:
        uploads.append(file)

    if not uploads:
        raise HTTPException(status_code=400, detail="No file(s) uploaded")

    # Validate and convert each image
    parts = []
    for up in uploads:
        ctype = (up.content_type or "image/jpeg").lower()
        if not ctype.startswith("image/"):
            raise HTTPException(status_code=415, detail=f"Unsupported content type: {ctype} for {up.filename}")
        data = await up.read()
        parts.append(types.Part.from_bytes(data=data, mime_type=ctype))

    # prompt adapts to multiple 
    count = len(parts)
    prompt = (
        f"You are given {count} photo(s) and spotify user data and their top 50 songs. "
        "Infer their **collective vibe** (mood, energy, aesthetics). "
        "Then recommend 5–8 songs in the format 'Song – Artist' that match that shared vibe while incorporating their own music taste. "
        "Output:\n"
        "• A 2 sentence vibe summary of the songs.\n"
        "• A numbered list of songs (Song – Artist)."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[*parts, prompt],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini error: {e}")

    text = getattr(response, "text", "") or ""
    summary, pairs = extract_summary_and_pairs(text)
    if not pairs:
        return jsonable_encoder({
            "count": count,
            "summary": summary,
            "pairs": [],
            "suggestions_text": text,
            "message": "No song lines detected from Gemini."
        })
    try:
        sp = set_up_spotify_client()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Spotify auth error: {e}")

    uris: List[str] = []
    misses: List[dict] = []
    for song, artist in pairs:
        try:
            uri = return_spotify_songs(artist=artist, song=song, market="US")
        except Exception as e:
            uri = None
        if uri:
            uris.append(uri)
        else:
            misses.append({"song": song, "artist": artist})

    if not uris:
        return jsonable_encoder({
            "count": count,
            "summary": summary,
            "pairs": pairs,
            "misses": misses,
            "suggestions_text": text, 
            "message": "Could not resolve any tracks on Spotify."
        })
#creating the playlist
    try:
        me = sp.current_user()
        user_id = me["id"]
        playlist_name = f"Vibe Mix {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        description = "Playlist generated from photo vibes + top tracks"
        playlist = sp.user_playlist_create(
            user=user_id,
            name=playlist_name,
            public=True,
            description=description
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Spotify playlist creation error: {e}")

 #adding the uris in baches of less than or equal to 100
    try:
        for i in range(0, len(uris), 100):
            add_tracks_to_playlist(playlist["id"], uris[i:i+100], sp=sp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Spotify add-tracks error: {e}")

    # get playlist Url
    playlist_url = playlist.get("external_urls", {}).get("spotify")
    playlist_public = playlist.get("public", True)
    playlist_display_name = playlist.get("name")

    # final output
    return jsonable_encoder({
        "count": count,
        "summary": summary,                 
        "pairs": pairs,                     
        "added_count": len(uris),           # how many we added
        "misses": misses,                   # any we couldn't find
        "playlist": {
            "id": playlist["id"],
            "name": playlist_display_name,
            "url": playlist_url,
            "public": playlist_public,
        },
        "suggestions_text": text,
    })

# @app.post("/")
# async def make_playlist(filedata: str = Form(...)):
#     load_dotenv()
#     api_key = os.getenv('GEMINI_KEY', 'default_key')

#     image_as_bytes = str.encode(filedata)  # convert string to bytes
#     img_recovered = base64.b64decode(image_as_bytes)

#     with open(filename, 'wb') as f:
#         # image_bytes = f.read()
#         f.write(img_recovered)

#     client = genai.Client(api_key=os.getenv('GEMINI_KEY', 'default_key'))

#     # when we do the actual api, make sure to change the mime_type so that it fits with the uploaders image
#     response = client.models.generate_content(
#         model='gemini-2.5-flash',
#         contents=[
#             types.Part.from_bytes(
#             data=f,
#             mime_type='image/jpeg',
#             ),
#             'You are posting this picture onto social media, such as Instagram. You want to add a song to the image that encapsulates the feeling that the image represents. Give a couple of song options.'
#         ]
#     )
#     print(response.text)
#     return jsonable_encoder(response.text)
#     # return {file.filename: "File received successfully"}

# import requests

# with open('test.jpg', 'rb') as f:
#     files = {'file': f}
#     response = requests.post('http://localhost:8000/', files=files)
#     print(response.json())