# CUNY Tech Prep Hacks: Aura Soundtrack
As part of CUNY Tech Prep Cohort 11, we participated in their hackathon and created Aura Soundtrack, an application that analyzes multiple images to generate a playlist of songs that matches the vibe of the images.

### Inspiration
Music and photos are both powerful ways to capture a moment, and we wanted to find a way to bring them together. On social media, people often share pictures and music, but choosing a song that really fits the mood can be difficult. Project Aura was created to make that process effortless. By analyzing the vibe of your images and combining it with your music taste, the app generates playlists that feel personal and unique. It’s not just about making posts more fun, but it’s also about discovering new songs, creating soundtracks for memories, and giving people a new way to express themselves through the combination of images and music.

### What it Does
* Users upload as many images as they’d like.
* They log into Spotify so we can personalize results with their listening data.
* The images and user data are analyzed with Gemini, which identifies the vibe from the photos and combines it with their top songs.
* The app then generates and displays a custom playlist that can be saved to the user’s Spotify account.


### How We Built It
We developed Project Aura with this tech stack:
* React: For the frontend framework, ensuring a responsive and user-friendly interface.
* Spotify API: To access user data, recommend songs tailored to their taste, and save playlists.
* Gemini API: Analyzes uploaded images to generate vibe-based playlist recommendations for users to listen to.
* FastAPI: The backend framework to connect everything together.

  
### Challenges We Face:
* Endless merge conflicts.
* Connecting the frontend and backend while integrating Gemini for image analysis.
* Creating playlists with Spotify API and displaying them using the Spotify iFrame API.
* Converting images from base64 into file objects for backend processing.


### Our Accomplishments
* Successfully displaying playlists that match the vibe of uploaded images.
* Smooth integration between Spotify and Gemini.
* Building a working end-to-end product under hackathon time constraints.


### What We Learned
One of our biggest takeaways was realizing how complex even small tasks, like adding a button to a website, can be once you dive into the code behind it. That gave us a greater appreciation for the technology we interact with every day and reminded us of just how much thought and effort goes into building it. We also saw how endless the possibilities are with coding because there’s so much creative freedom in taking an idea and bringing it to life with nothing more than a laptop.

We also learned the value of teamwork. Having a strong team that trusts and relies on each other made it possible for us to solve problems, handle setbacks, and keep pushing forward. Collaboration and communication were just as essential as technical skills, and they’re what truly turned our project into a success.

Finally, this project taught us the importance of persistence. Coding often means failing, debugging, and trying again, sometimes dozens of times. But pushing through those failures and exploring every possible solution makes the reward so much greater when the code finally works. It reminded us that failure isn’t the end, but a necessary step toward success.

### Next Steps for Aura Soundtrack
* Deploy the app so others can use it.
* Request Spotify permissions to automatically save playlists to users’ accounts.
* Add caching mechanisms to improve analysis speed. 
* Implement user history so people are able to revisit past photo uploads and playlists. 
* Expand integration by connecting with other platforms like Apple Music, Youtube Music and SoundCloud
