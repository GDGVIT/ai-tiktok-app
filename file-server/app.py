# File server in flask with asynchronous support that has endpoints: (all of this works on json only)
# 1. /images - Takes in a list of keywords, gets images and downloads them in /static/images and returns a list of images urls (from local storage)
# 2. /images/urls - Returns a list of image urls (from local storage)
# 3. /voiceover - Takes in a text and generates a voiceover and returns the url of the voiceover (from local storage) that's downloadable
# 5. /movie - Takes in a list of image urls and a voiceover url and generates a movie and returns the url of the movie (from local storage) that's downloadable


# Path: file-server/app.py
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import asyncio

load_dotenv()

PORT = os.environ["FILE_SERVER_PORT"]
app = Flask(__name__)
CORS(app)


import requests

async def search_images(api_key, keywords, per_page=1):
    """
    Search for images based on keywords using the Pexels API.

    Parameters:
    - api_key (str): Pexels API key for authorization.
    - keywords (list): List of keywords for image search.
    - per_page (int): Number of images per page.

    Returns:
    - list: List of image URLs.
    """
    url = "https://api.pexels.com/v1/search"
    headers = {
        "Authorization": api_key,
    }

    image_urls = []

    for keyword in keywords:
        params = {
            "query": keyword,
            "per_page": per_page,
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            photos = data.get("photos", [])

            if not photos:
                print(f"No photos found for keyword: {keyword}")
            else:
                # Get the first photo's original image URL for each keyword
                image_urls.append(photos[0]["src"]["original"])

        else:
            print(f"Error for keyword {keyword}: {response.status_code}")

    return image_urls



async def download_images(url_list, out_dir):
    """
    Download images from a list of URLs and save them to the specified directory.

    Parameters:
    - url_list (list): List of image URLs to download.
    - out_dir (str): Output directory to save the downloaded images.

    Returns:
    - None
    """
    # Create the output directory if it doesn't exist
    os.makedirs(out_dir, exist_ok=True)

    for url in url_list:
        response = requests.get(url)

        if response.status_code == 200:
            # Get the file name from the URL
            filename = os.path.join(out_dir, os.path.basename(url))

            # Save the image to the specified output directory
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Image downloaded: {filename}")
        else:
            print(
                f"Failed to download image from {url}. Status code: {response.status_code}"
            )


@app.route("/images", methods=["POST", "GET"])
async def images():
    """
    Takes in a list of keywords, gets images and downloads them in /static/images
    and returns a list of images URLs (from local storage).
    """
    if request.method == "POST":
        json_data = json.loads(request.data.decode("utf-8"))
        keywords = json_data["keywords"]

        img_urls = await search_images(os.environ["PEXELSAPI"], keywords)
        await download_images(img_urls, "static/images")

        images = os.listdir("static/images")
        # Convert images to URLs
        images_urls = [f"http://localhost:{PORT}/static/images/{image}" for image in images]
        return jsonify({"image_urls": images_urls})
    else:
        # Return a list of image URLs from static/images
        images = os.listdir("static/images")
        # Convert images to URLs
        images_urls = [f"http://localhost:{PORT}/static/images/{image}" for image in images]
        return jsonify({"image_urls": images_urls})

# Routes for voiceover generation
from gtts import gTTS
import os


async def generate_voiceover(text, output_file="output_voiceover.mp3"):
    """
    Generate a voiceover from text and save it as an audio file.

    Args:
        text (str): The text to convert to speech.
        output_file (str): The name of the output audio file (default: "output_voiceover.mp3").
    """
    # Initialize the TTS object
    tts = gTTS(text)

    # Save the speech as an audio file
    tts.save(output_file)

    # Play the generated audio (optional)
    os.system(f"mpg321 {output_file}")  # You can use other audio players if needed

@app.route("/voiceover", methods=["POST"])
async def voiceover():
    """
    Takes in a text and generates a voiceover and returns the url of the voiceover
    (from local storage) that's downloadable.
    """
    if request.method == "POST":
        json_data = json.loads(request.data.decode("utf-8"))
        text = json_data["text"]

        # Generate the voiceover
        await generate_voiceover(text, "file-server/static/audio/output_voiceover.mp3")

        # Return the URL of the voiceover
        return jsonify({"voiceover_url": f"http://localhost:{PORT}/static/audio/output_voiceover.mp3"})

# Routes for movie generation


# First we have to generate the movie

if __name__ == "__main__":
    app.run(debug=True)
