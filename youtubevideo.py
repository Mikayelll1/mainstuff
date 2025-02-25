# DISCLAIMER!!!!
# Under no circumstance should this project be used to download content from youtube without the original author's permission, this is just a simple project to start with
# Use of this project implies you are complying with the Copyright laws that YouTube has set in place

from pytubefix import YouTube
import streamlit as st

def Download(link_video):
    youtubeObject = YouTube(link_video)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("An error has occurred")
    print("Download is successful")

st.title("YouTube Video Downloader")
link_video = st.text_input("Enter the URL of the YouTube Video")
if st.button("Download"):
    Download(link_video=link_video)

youtubeObject.on_complete
