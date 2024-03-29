import streamlit as st
from pytube import YouTube
import os
import threading
import time


def download_audio(url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()

    if audio_stream:
        output_file = audio_stream.download()
        base, ext = os.path.splitext(output_file)
        new_file = base + '.mp3'
        os.rename(output_file, new_file)
        st.success("Download completed")

        with open(new_file, "rb") as file:
            mp3_content = file.read()

        st.download_button(label="Download", data=mp3_content, file_name="audio.mp3", mime="audio/mp3")

        # Start a separate thread to delete mp3 files every 10 minutes
        delete_thread = threading.Thread(target=schedule_delete_mp3_files, args=(2,))
        delete_thread.start()

    else:
        st.error("No audio stream found")


def delete_mp3_files():
    current_directory = os.getcwd()
    for file_name in os.listdir(current_directory):
        if file_name.endswith(".mp3"):
            file_path = os.path.join(current_directory, file_name)
            os.remove(file_path)
    st.success("All downloaded mp3 files have been deleted")


def schedule_delete_mp3_files(interval):
    while True:
        time.sleep(interval * 60)  # Convert minutes to seconds
        delete_mp3_files()


def main():
    st.title("Youtube Audio Downloader")
    url = st.text_input("Enter the URL of the video")
    if st.button("Download"):
        download_audio(url)


if __name__ == "__main__":
    main()