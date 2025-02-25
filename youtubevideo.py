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