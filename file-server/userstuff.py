import uuid
import os


# Generate uuid for user
def generate_uuid():
    return str(uuid.uuid4())[0:8]


# Generate folder structure with uuid and audio, movie and images as subfolders
def generate_folder_structure(c):
    os.mkdir(f"./static/{c}")
    os.mkdir(f"./static/{c}/audio")
    os.mkdir(f"./static/{c}/movie")
    os.mkdir(f"./static/{c}/images")


# Remove folder structure with uuid and audio, movie and images as subfolders
def remove_folder_structure(c):
    os.rmdir(f"./static/{c}/audio")
    os.rmdir(f"./static/{c}/movie")
    os.rmdir(f"./static/{c}/images")
    os.rmdir(f"./static/{c}")
