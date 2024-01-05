import os
from moviepy.editor import AudioFileClip, ImageSequenceClip, concatenate_videoclips
from PIL import Image


def resize_images(folder_path):
    """
    Resize all images in the given folder to a 16:9 portrait ratio and overwrite them.

    Parameters:
    - folder_path (str): The path to the folder containing the images.
    """
    # Ensure the folder path is valid
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        return

    # Get a list of all files in the folder
    files = os.listdir(folder_path)

    # Filter only image files
    image_files = [
        file
        for file in files
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))
    ]

    # Resize and overwrite each image
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)

        # Open the image
        with Image.open(image_path) as img:
            # Calculate the new width based on a 16:9 ratio
            new_width = int(img.height * (9 / 16))

            # Resize the image to the new dimensions
            resized_img = img.resize((new_width, img.height))

            # Overwrite the original image
            resized_img.save(image_path)

    return folder_path


def create_video(
    audio_file,
    image_folder,
    output_file,
):
    img_folder = resize_images(image_folder)
    image_files = [
        os.path.join(image_folder, img) for img in sorted(os.listdir(image_folder))
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
