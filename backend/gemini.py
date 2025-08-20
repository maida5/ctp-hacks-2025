from google import genai
from dotenv import load_dotenv
from google.genai import types
import os

load_dotenv()
api_key = os.getenv('GEMINI_KEY', 'default_key')

with open('test.jpg', 'rb') as f:
    image_bytes = f.read()

client = genai.Client(api_key=os.getenv('GEMINI_KEY', 'default_key'))

# when we do the actual api, make sure to change the mime_type so that it fits with the uploaders image
response = client.models.generate_content(
model='gemini-2.5-flash',
contents=[
    types.Part.from_bytes(
    data=image_bytes,
    mime_type='image/jpeg',
    ),
    'You are posting this picture onto social media, such as Instagram. You want to add a song to the image that encapsulates the feeling that the image represents. Give a couple of song options.'
]
)

print(response.text)

# # The client gets the API key from the environment variable `GEMINI_API_KEY`.
# client = genai.Client(api_key=os.getenv('GEMINI_KEY', 'default_key'))

# response = client.models.generate_content(
#     model="gemini-2.5-flash", contents="Explain how AI works in a few words"
# )
# print(response.text)