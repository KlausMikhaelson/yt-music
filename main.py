import streamlit as st
from pytube import YouTube
import os

def download_audio(url):
    yt = YouTube(url)
    audio_stream= yt.streams.filter(only_audio=True).first()

    if audio_stream:
        output_file = audio_stream.download()
        base,ext = os.path.splitext(output_file)
        new_file = base + '.mp3'
        os.rename(output_file,new_file)
        st.success("Download completed")

        with open(new_file, "rb") as file:
            mp3_content=file.read()

        st.download_button(label="Download",data=mp3_content, file_name="audio.mp3", mime="audio/mp3")
    else:
        st.error("No audio stream found")
    
def main():
    st.title("Youtube Audio Downloader")
    url = st.text_input("Enter the URL of the video")
    if st.button("Download"):
        download_audio(url)

if __name__ == "__main__":
    main()