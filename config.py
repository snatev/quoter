from os import makedirs, path

def create_directory(fpath):
    makedirs(fpath, exist_ok=True)

def create_file_if_not_exists(fpath, default_content=""):
    if not path.exists(fpath) or not path.isfile(fpath):
        with open(fpath, "w", encoding="utf-8") as file:
            file.write(default_content)

BASE_DIR = path.dirname(path.abspath(__file__))
create_directory(path.join(BASE_DIR, "static"))
create_directory(path.join(BASE_DIR, "folders"))

LAST_FILE = path.join(BASE_DIR, "static/last.txt")
QUOTES_FILE = path.join(BASE_DIR, "static/quotes.txt")
VIDEO_DIRECTORY = path.join(BASE_DIR, "folders/videos")
MUSIC_DIRECTORY = path.join(BASE_DIR, "folders/musics")
OUTPUT_DIRECTORY = path.join(BASE_DIR, "folders/final_video")
SAVED_VIDEO_DIRECTORY = path.join(BASE_DIR, "folders/saved_videos")

directories = [VIDEO_DIRECTORY, MUSIC_DIRECTORY, OUTPUT_DIRECTORY, SAVED_VIDEO_DIRECTORY]
for directory in directories: create_directory(directory)

create_file_if_not_exists(LAST_FILE, "0")
create_file_if_not_exists(QUOTES_FILE, "Test Quote 1 - Snatev\n")
