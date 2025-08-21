from google import genai
from dotenv import load_dotenv
from google.genai import types
import os
from get_spotify_data import get_spotify_top_songs

load_dotenv()
api_key = os.getenv('GEMINI_KEY', 'default_key')

with open('stassi2.jpg', 'rb') as f:
    image_bytes = f.read()

client = genai.Client(api_key=os.getenv('GEMINI_KEY', 'default_key'))

top_songs = get_spotify_top_songs()

# when we do the actual api, make sure to change the mime_type so that it fits with the uploaders image
response = client.models.generate_content(
model='gemini-2.5-flash',
contents=[
    types.Part.from_bytes(
    data=image_bytes,
    mime_type='image/jpeg',
    ),
    f'You are posting this picture onto social media, such as Instagram. You want to add a song to the image that encapsulates the feeling that the image represents, but you also want it to be representative of you. Here are your last top 50 songs, {top_songs}. Give a couple of song options that follow your music taste but also fit the feeling that the picture gives off. You can give songs outside of the list, but it has to be similar to the songs on the list.'
]
)

print(response.text)

# # The client gets the API key from the environment variable `GEMINI_API_KEY`.
# client = genai.Client(api_key=os.getenv('GEMINI_KEY', 'default_key'))

# response = client.models.generate_content(
#     model="gemini-2.5-flash", contents="Explain how AI works in a few words"
# )
# print(response.text)