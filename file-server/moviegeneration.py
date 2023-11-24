import os
from PIL import Image
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, ImageSequenceClip, concatenate_videoclips
import cv2

def resize_images(image_folder, target_height):
    # Get the list of image files in the folder
    image_files = [f"{image_folder}/{img}" for img in sorted(
        os.listdir(image_folder)) if img.endswith(".jpeg")]

    # Resize and overwrite each image in the folder
    for image_file in image_files:
        img = Image.open(image_file)
        width, height = img.size
        target_width = int(width * (target_height / height))

        # Resize while maintaining the aspect ratio
        resized_img = img.resize(
            (target_width, target_height), Image.ANTIALIAS)

        # Crop to maintain the 9:16 aspect ratio
        crop_width = min(target_width, target_height * 9 // 16)
        crop_height = min(target_height, target_width * 16 // 9)
        left = (target_width - crop_width) // 2
        top = (target_height - crop_height) // 2
        cropped_img = resized_img.crop(
            (left, top, left + crop_width, top + crop_height))

        # Save the modified image, overwriting the original
        cropped_img.save(image_file)

def create_video(image_folder, audio_file, output_file):
    # Get the list of resized image files in the folder
    image_files = [f"{image_folder}/{img}" for img in sorted(os.listdir(image_folder)) ]

    # Get the duration of the audio file
    audio_clip = AudioFileClip(audio_file)
    audio_duration = audio_clip.duration

    # Calculate the duration each image should be displayed
    num_images = len(image_files)
    duration_per_image = audio_duration / num_images

    # Create a list of image clips from the resized images
    image_clips = [ImageSequenceClip([image_file], fps=1 / duration_per_image) for image_file in image_files]

    # Concatenate the image clips into a video
    video_clip = concatenate_videoclips(image_clips, method="compose")

    # Set the duration of the video to match the total duration
    video_clip = video_clip.set_duration(audio_duration)

    # Set the audio of the video clip to the provided audio clip
    video_clip = video_clip.set_audio(audio_clip)

    # Write the final video with audio
    output_video_file = output_file.replace('.mp4', '_with_audio.mp4')
    video_clip.write_videofile(output_video_file, codec='libx264', audio_codec='aac')

# resize_images("file-server/static/images", 1080)
# create_video("./stati", "file-server/static/audio/output_voiceover.mp3","file-server/static/movie/output_video.mp4")