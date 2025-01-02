import os
import random
from moviepy.editor import AudioFileClip, VideoFileClip
from moviepy.audio.fx.all import audio_fadein, audio_fadeout

class MusicManager:
    def __init__(self, music_dir):
        self.music_dir = music_dir

    def select_random_music(self):
        music_files = [f for f in os.listdir(self.music_dir) if f.lower().endswith((".mp3", ".wav"))]
        return os.path.join(self.music_dir, random.choice(music_files)) if music_files else None

    def add_music_to_video(self, video_path, output_path, fade_duration=1):
        music_path = self.select_random_music()
        if not music_path:
            print("No Music Found")
            exit()

        with VideoFileClip(video_path) as video, AudioFileClip(music_path) as music:
            video_duration = video.duration

            if music.duration <= video_duration:
                music_segment = music.set_duration(video_duration)
            else:
                max_start_time = music.duration - video_duration
                start_time = random.uniform(0, max_start_time)
                music_segment = music.subclip(start_time, start_time + video_duration)

            music_segment = audio_fadein(music_segment, fade_duration)
            music_segment = audio_fadeout(music_segment, fade_duration)

            video_with_music = video.set_audio(music_segment)
            video_with_music.write_videofile(output_path, codec="libx264", audio_codec="aac")
