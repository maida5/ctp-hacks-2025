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

@app.get("/hello")
def root():
    print("Hello World")
    return {"message": "Hello World"}

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    # validating the input/ error handeling
    if not file:
        raise HTTPException(400, "No file uploaded")
    content_type = file.content_type or "image/jpeg"
    if not content_type.startswith("image/"):
        raise HTTPException(415, f"Unsupported content type: {content_type}")

    # read file 
    image_bytes = await file.read()

    # call gemini
    prompt = (
        "You are posting this picture on social media. "
        "Suggest 3–5 specific song titles with artists that match the vibe. "
        "Return a simple numbered list like:\n"
        "1) Song - Artist\n2) Song - Artist"
    )
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=content_type),
                prompt,
            ],
        )
    except Exception as e:
        raise HTTPException(500, f"Gemini error: {e}")

    text = getattr(response, "text", "") or ""
    return jsonable_encoder({
        "filename": file.filename,
        "suggestions_text": text
    })
# @app.post("/")
# async def make_playlist(file: UploadFile = File(...)):
#     # load_dotenv()
#     # api_key = os.getenv('GEMINI_KEY', 'default_key')

#     # with open('test.jpg', 'rb') as f:
#     #     image_bytes = f.read()

#     # client = genai.Client(api_key=os.getenv('GEMINI_KEY', 'default_key'))

#     # # when we do the actual api, make sure to change the mime_type so that it fits with the uploaders image
#     # response = client.models.generate_content(
#     #     model='gemini-2.5-flash',
#     #     contents=[
#     #         types.Part.from_bytes(
#     #         data=image_bytes,
#     #         mime_type='image/jpeg',
#     #         ),
#     #         'You are posting this picture onto social media, such as Instagram. You want to add a song to the image that encapsulates the feeling that the image represents. Give a couple of song options.'
#     #     ]
#     # )
#     # console.log(response.text)
#     # return jsonable_encoder(response.text)
#     return {file.filename: "File received successfully"}

# import requests

# with open('test.jpg', 'rb') as f:
#     files = {'file': f}
#     response = requests.post('http://localhost:8000/', files=files)
#     print(response.json())