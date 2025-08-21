from fastapi import FastAPI, UploadFile, File, Form
# import google
from google import genai
from dotenv import load_dotenv
from google.genai import types
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import os

import requests

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["https://ctp-hacks-2025-maida5s-projects.vercel.app/","https://ctp-hacks-2025-maida5-maida5s-projects.vercel.app/"],  # Or specify your frontend URL
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello")
def root():
    console.log("Hello World")
    return {"message": "Hello World"}

@app.post("/")
async def make_playlist(filedata: str = Form(...)):
    print(await request.body())  # Log the raw request body
    print(request.headers)       # Log the request headers

    load_dotenv()
    api_key = os.getenv('GEMINI_KEY', 'default_key')

    image_as_bytes = str.encode(filedata)  # convert string to bytes
    img_recovered = base64.b64decode(image_as_bytes)

    with open(filename, 'wb') as f:
        # image_bytes = f.read()
        f.write(img_recovered)

    client = genai.Client(api_key=os.getenv('GEMINI_KEY', 'default_key'))

    # when we do the actual api, make sure to change the mime_type so that it fits with the uploaders image
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            types.Part.from_bytes(
            data=f,
            mime_type='image/jpeg',
            ),
            'You are posting this picture onto social media, such as Instagram. You want to add a song to the image that encapsulates the feeling that the image represents. Give a couple of song options.'
        ]
    )
    print(response.text)
    return jsonable_encoder(response.text)
    # return {file.filename: "File received successfully"}

# import requests

# with open('test.jpg', 'rb') as f:
#     files = {'file': f}
#     response = requests.post('http://localhost:8000/', files=files)
#     print(response.json())