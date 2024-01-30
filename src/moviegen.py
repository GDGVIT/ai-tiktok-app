import os
from moviepy.editor import AudioFileClip, ImageSequenceClip, concatenate_videoclips
from PIL import Image
import concurrent.futures
from functools import partial
import multiprocessing

def resize_image_parallel(image_path):
    with Image.open(image_path) as img:
        new_width = int(img.height * (9 / 16))
        resized_img = img.resize((new_width, img.height))
        resized_img.save(image_path)

def resize_images(folder_path):
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        return

    files = os.listdir(folder_path)
    image_files = [
        os.path.join(folder_path, file)
        for file in files
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(resize_image_parallel, image_files)

    return folder_path



def create_video(
    audio_file,
    image_folder_path,  # Change the parameter name here
    output_file,
):
    img_folder = resize_images(image_folder_path)  # Change the argument here
    image_files = [
        os.path.join(image_folder_path, img) for img in sorted(os.listdir(image_folder_path))
    ]
    audio_clip = AudioFileClip(audio_file)
    audio_duration = audio_clip.duration
    num_images = len(image_files)
    duration_per_image = audio_duration / num_images
    image_clips = [
        ImageSequenceClip([image_file], fps=1 / duration_per_image)
        for image_file in image_files
    ]
    video_clip = concatenate_videoclips(image_clips, method="compose")
    video_clip = video_clip.set_duration(audio_duration)
    # video_clip = video_clip.resize(width=900, height=1600)
    video_clip = video_clip.set_audio(audio_clip)
    output_video_file = output_file.replace(".mp4", ".mp4")
    video_clip.write_videofile(
        output_video_file,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="ultrafast",
    )
    return output_video_file

