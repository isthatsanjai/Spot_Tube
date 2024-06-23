import os
from pytube import YouTube
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def download_video_as_mp3(url):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path="C:/Users\sanja\Downloads")
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        logger.info(f"Downloaded and converted to MP3: {new_file}")
        return new_file
    except Exception as e:
        logger.error(f"Error downloading the video: {e}")
        return None


def main():
    link = input("Enter URL: ")
    download_video_as_mp3(link)


if __name__ == "__main__":
    main()
