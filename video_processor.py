import cv2
from np import array
from os import makedirs

from PIL import Image
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype

from moviepy.video.fx.all import fadein, fadeout
from moviepy.audio.fx.all import audio_fadein, audio_fadeout
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip

class VideoProcessor:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        makedirs(self.output_dir, exist_ok=True)

    def trim_to_duration(self, input_path, output_path, duration=10):
        with VideoFileClip(input_path) as video:
            if video.duration > duration:
                trimmed_video = video.subclip(0, duration)
                trimmed_video.write_videofile(output_path, codec="libx264", audio_codec=None)
            else: video.write_videofile(output_path, codec="libx264", audio_codec=None)

    def resize_and_overlay(self, input_path, output_path, target_aspect_ratio=(9, 16)):
        video = VideoFileClip(input_path)

        width, height = video.size
        target_width, target_height = target_aspect_ratio
        target_ratio = target_width / target_height

        if (width / height) > target_ratio:
            video = video.crop(width=height * target_ratio, height=height, x_center=width / 2, y_center=height / 2)
        else: video = video.crop(width=width, height=width / target_ratio, x_center=width / 2, y_center=height / 2)

        overlay = ColorClip(size=video.size, color=(0, 0, 0), duration=video.duration).set_opacity(0.5)

        composite = CompositeVideoClip([video, overlay])
        composite.write_videofile(output_path, codec="libx264", audio_codec=None)

        video.close()
        composite.close()

    def add_fades(self, video_path, output_path, fade_duration=1):
        try:
            with VideoFileClip(video_path) as video:
                faded_video = fadein(video, duration=fade_duration).fx(fadeout, duration=fade_duration)

                if video.audio:
                    faded_audio = audio_fadein(video.audio, duration=fade_duration).fx(audio_fadeout, duration=fade_duration)
                    faded_video = faded_video.set_audio(faded_audio)

                faded_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
        except Exception as e: print(e)

    def add_text(self, video_path, text, output_path, stroke_width=2, stroke_fill="black", text_opacity=0.75, brand_name="QUOTER SHORTS"):
        text = text.replace('"', '')

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened(): raise IOError("Could Not Open Video")

        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        def sanitize_text(text):
            return text.encode("ascii", "ignore").decode("ascii").replace("'", "'")

        def wrap_text(text, font, max_width):
            lines = []
            current_line = ""
            words = text.split(" ")

            for word in words:
                test_line = current_line + word + " "
                text_width = font.getbbox(test_line.strip())[2]

                if text_width <= max_width: current_line = test_line
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "

            lines.append(current_line.strip())
            return lines

        sanitized_text = sanitize_text(text)
        font = truetype("./static/Roboto-Regular.ttf", 55)
        brand_font = truetype("./static/Roboto-Black.ttf", 125)

        if " - " in sanitized_text:
            main_text, author = sanitized_text.rsplit(" - ", 1)
            author = " - " + author
        else: main_text, author = sanitized_text, ""

        quote_lines = wrap_text(main_text, font, width - 100)
        author_lines = wrap_text(author, font, width - 100) if author else []
        lines = quote_lines + ["", "", "", "", ""] + author_lines

        while True:
            ret, frame = cap.read()
            if not ret: break

            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            text_overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
            draw = Draw(text_overlay)

            brand_text_width, brand_text_height = brand_font.getbbox(brand_name)[2:]
            brand_x = (width - brand_text_width) // 2
            brand_y = 20

            draw.text((brand_x, brand_y), brand_name, font=brand_font, fill=(255, 255, 255, int(255 * 0.1)))

            text_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] + 10 for line in lines)
            y_position = (height - text_height) // 2

            for line in lines:
                bbox = font.getbbox(line)
                text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
                x_position = (width - text_width) // 2

                draw.text(
                    (x_position, y_position), line, font=font,
                    fill=(255, 255, 255, int(255 * text_opacity)),
                    stroke_width=stroke_width, stroke_fill=stroke_fill)

                y_position += text_height + 10

            blended_image = Image.alpha_composite(image.convert("RGBA"), text_overlay)
            frame_with_text = cv2.cvtColor(array(blended_image.convert("RGB")), cv2.COLOR_RGB2BGR)
            out.write(frame_with_text)

        cap.release()
        out.release()
