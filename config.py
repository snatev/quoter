import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LAST_FILE = os.path.join(BASE_DIR, "last.txt")
VIDEO_DIRECTORY = os.path.join(BASE_DIR, "videos")
MUSIC_DIRECTORY = os.path.join(BASE_DIR, "musics")
QUOTES_FILE = os.path.join(BASE_DIR, "quotes.txt")
OUTPUT_DIRECTORY = os.path.join(BASE_DIR, "final_video")
SAVED_VIDEO_DIRECTORY = os.path.join(BASE_DIR, "saved_videos")

os.makedirs(VIDEO_DIRECTORY, exist_ok=True)
os.makedirs(MUSIC_DIRECTORY, exist_ok=True)
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
os.makedirs(SAVED_VIDEO_DIRECTORY, exist_ok=True)

if not os.path.exists(LAST_FILE):
    with open(LAST_FILE, "w", encoding="utf-8") as file: file.write("0")

if not os.path.exists(QUOTES_FILE):
    with open(QUOTES_FILE, "w", encoding="utf-8") as file: file.write("Test Quote 1\n")
