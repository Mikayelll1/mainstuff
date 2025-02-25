# DISCLAIMER!!!!
# Under no circumstance should this project be used to download content from youtube without the original author's permission, this is just a simple project to start with
# Use of this project implies you are complying with the Copyright laws that YouTube has set in place

# downloading youtube audio from a youtube link using streamlit.
from pytubefix import YouTube
import streamlit as st

#function to define 
def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_audio_only()
    try:
        youtubeObject.download()
    except:
        print("An error has occurred")
    print("Download is successful")

st.title("YouTube Video Downloader")
link = st.text_input("Enter the URL of the YouTube Video")
if st.button("Download"):
    Download(link)
