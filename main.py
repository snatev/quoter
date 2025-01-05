import argparse
from random import choice
from shutil import rmtree
from os import path, listdir, makedirs

from config import *
from quote_manager import QuoteManager
from music_manager import MusicManager
from video_processor import VideoProcessor

def main():
    parser = argparse.ArgumentParser(description="Generate Short Videos With Quotes And Music")
    parser.add_argument("--filter-quote", action="store_true", help="Remove Duplicate Quotes")
    parser.add_argument("--video", type=str, help="Specify Video To Use")
    args = parser.parse_args()

    quote_manager = QuoteManager(QUOTES_FILE, LAST_FILE)
    video_processor = VideoProcessor(OUTPUT_DIRECTORY)
    music_manager = MusicManager(MUSIC_DIRECTORY)

    if args.filter_quote:
        quote_manager.remove_duplicate_quotes()
        print("Duplicate Quotes Removed")
        return

    quote = quote_manager.get_next_quote()
    if not quote:
        print("No More Quotes Available")
        return

    if not listdir(VIDEO_DIRECTORY):
        print("Video Directory Is Empty")
        return

    if not listdir(MUSIC_DIRECTORY):
        print("Music Directory Is Empty")

    if path.exists(OUTPUT_DIRECTORY):
        rmtree(OUTPUT_DIRECTORY)
    makedirs(OUTPUT_DIRECTORY)

    video_file = args.video or choice(listdir(VIDEO_DIRECTORY))
    input_video_path = path.join(VIDEO_DIRECTORY, video_file)
    trimmed_video_path = path.join(OUTPUT_DIRECTORY, f"trimmed_{video_file}")

    video_processor.trim_to_duration(input_video_path, trimmed_video_path)
    resized_video_path = path.join(OUTPUT_DIRECTORY, f"resized_{video_file}")
    video_processor.resize_and_overlay(trimmed_video_path, resized_video_path)

    text_video_path = path.join(OUTPUT_DIRECTORY, f"text_{video_file}")

    video_processor.add_text(
        resized_video_path,
        quote, text_video_path,
        stroke_width=0, stroke_fill="black")

    final_video_path = path.join(OUTPUT_DIRECTORY, f"final_{video_file}")
    music_manager.add_music_to_video(text_video_path, final_video_path, 2)
    final_with_fades_path = path.join(SAVED_VIDEO_DIRECTORY, f"{video_file}")

    try: video_processor.add_fades(final_video_path, final_with_fades_path, 2)
    except OSError as e: print(e)

    rmtree(OUTPUT_DIRECTORY)
    print(f"Final Video Saved To {final_with_fades_path}")

if __name__ == "__main__":
    main()
