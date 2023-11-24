# File server in flask with asynchronous support that has endpoints: (all of this works on json only)
# 1. /images - Takes in a list of keywords, gets images and downloads them in /static/images and returns a list of images urls (from local storage)
# 2. /images/urls - Returns a list of image urls (from local storage)
# 3. /voiceover - Takes in a text and generates a voiceover and returns the url of the voiceover (from local storage) that's downloadable
# 5. /movie - Takes in a list of image urls and a voiceover url and generates a movie and returns the url of the movie (from local storage) that's downloadable


# Path: file-server/app.py
import os
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from imgget import *
import voiceovergen as vo
import moviegeneration as mg

load_dotenv()

PORT = os.environ["FILE_SERVER_PORT"]
app = Flask(__name__)
CORS(app)


@app.route("/text", methods=["POST"])
async def text():
    """Send prompt to palm 2 API, get text. Use keywords to get images."""
    pass


@app.route("/edittext", methods=["POST"])
async def edittext():
    """User sends back the edited text, converted to voiceover and movie."""
    pass


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
        image_urls = [f"http://localhost:{PORT}/static/images/{image}" for image in images]
        return jsonify({"image_urls": image_urls})
    else:
        images = os.listdir("static/images")
        image_urls = [f"http://localhost:{PORT}/static/images/{image}" for image in images]
        return jsonify({"image_urls": image_urls})


@app.route("/voiceover", methods=["POST"])
async def voiceover():
    """
    Takes in a text and generates a voiceover and returns the url of the voiceover
    (from local storage) that's downloadable.
    """
    if request.method == "POST":
        json_data = json.loads(request.data.decode("utf-8"))
        text = json_data["text"]

        if not os.path.exists("file-server/static/audio/output_voiceover.mp3"):
            await vo.generate_voiceover(text, "file-server/static/audio/output_voiceover.mp3")

        return jsonify({"voiceover_url": f"http://localhost:{PORT}/static/audio/output_voiceover.mp3"})


@app.route("/movie", methods=["POST"])
async def movie():
    """
    Takes in a list of image URLs and a voiceover URL and generates a movie and returns the URL of the movie
    (from local storage) that's downloadable.
    """
    if request.method == "POST":
        image_folder = "file-server/static/images"
        audio_file = "file-server/static/audio/output_voiceover.mp3"

        await mg.create_video(image_folder, audio_file, "file-server/static/movie/output_movie.mp4")

        return jsonify({"movie_url": f"http://localhost:{PORT}/static/movie/output_movie.mp4"})

# /reset = deletes all files in static/images, static/audio, static/movie
@app.route("/reset", methods=["POST"])
async def reset():
    """
    Deletes all files in static/images, static/audio, static/movie.
    """
    if request.method == "POST":
        # recursively go through all files in static and delete only the files
        for root, dirs, files in os.walk("./static"):
            for file in files:
                os.remove(os.path.join(root, file))


        return jsonify({"message": "All files deleted."})

if __name__ == "__main__":
    app.run(debug=True)
