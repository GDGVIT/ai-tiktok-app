# Path: file-server/app.py
import os
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from imgget import *
import voiceovergen as vo
import moviegen as mg
import llm_req as llm
import time
import asyncio
load_dotenv()

PORT = os.environ["FILE_SERVER_PORT"]
app = Flask(__name__)
CORS(app)
PALM_API_KEY = os.environ["PALMAPI"]


@app.route("/text", methods=["POST"])
def text():
    """Send prompt to palm 2 API, get text. Use keywords to get images."""
    if request.method == 'POST':
        data = json.loads(request.data.decode("utf-8"))
        keywords = data["keywords"]
        img_urls = search_images(os.environ["PEXELSAPI"], 2*keywords)
        download_images(img_urls, "static/images")
        images = os.listdir("file-server/static/images")
        text = llm.generate_text(
            "Write a 1 minute info speech in plaintext for :" + data["text"])
        return jsonify({"text": text, "image_urls": [f"http://localhost:{PORT}/static/images/{image}" for image in images]})


@app.route("/edittext", methods=["POST"])
def edittext():
    """
    Takes in a text, generates a voiceover, and creates a video with the voiceover.
    Returns the URL of the generated video.
    """
    if request.method == 'POST':
        data = json.loads(request.data.decode("utf-8"))
        edit_text = data["text"]
        vo_url = vo.generate_voiceover(str(edit_text))

        # vo_url = 'file-server/static/audio/output_voiceover.mp3'
        # check if file exists at vo_url
        if not os.path.exists(vo_url):
            vo_url = vo.generate_voiceover(
                edit_text, "file-server/static/audio/output_voiceover.mp3")

        print(vo_url)
        video_url = mg.create_video(vo_url)
        return jsonify({"video_url": f"http://localhost:{PORT}/static/movie/output_video_with_audio.mp4"})


@app.route("/images", methods=["POST", "GET"])
def images():
    """
    Takes in a list of keywords, gets images and downloads them in /static/images
    and returns a list of images URLs (from local storage).
    """
    if request.method == "POST":
        json_data = json.loads(request.data.decode("utf-8"))
        keywords = json_data["keywords"]

        img_urls = search_images(os.environ["PEXELSAPI"], keywords)
        download_images(img_urls, "file-server/static/images")

        images = os.listdir("file-server/static/images")
        image_urls = [
            f"http://localhost:{PORT}/static/images/{image}" for image in images]
        return jsonify({"image_urls": image_urls})
    else:
        images = os.listdir("static/images")
        image_urls = [
            f"http://localhost:{PORT}/static/images/{image}" for image in images]
        return jsonify({"image_urls": image_urls})


@app.route("/voiceover", methods=["POST"])
def voiceover():
    """
    Takes in a text and generates a voiceover and returns the url of the voiceover
    (from local storage) that's downloadable.
    """
    if request.method == "POST":
        json_data = json.loads(request.data.decode("utf-8"))
        text = json_data["text"]

        # if not os.path.exists("file-server/static/audio/output_voiceover.mp3"):
        #     vo.generate_voiceover(
        #         text, "file-server/static/audio/output_voiceover.mp3")
        vo_url = vo.generate_voiceover(text, "file-server/static/audio/output_voiceover.mp3")
        print(vo_url)
        return jsonify({"voiceover_url": f"http://localhost:{PORT}/static/audio/output_voiceover.mp3"})


@app.route("/movie", methods=["POST"])
def movie():
    """
    Takes in a list of image URLs and a voiceover URL and generates a movie and returns the URL of the movie
    (from local storage) that's downloadable.
    """
    if request.method == "POST":
        image_folder = "file-server/static/images"
        audio_file = "file-server/static/audio/output_voiceover.mp3"

        mg.create_video(image_folder, audio_file,
                        "file-server/static/movie/output_movie.mp4")

        return jsonify({"movie_url": f"http://localhost:{PORT}/static/movie/output_movie.mp4"})

# /reset = deletes all files in static/images, static/audio, static/movie


@app.route("/reset", methods=["POST"])
def reset():
    """
    Deletes all files in static/images, static/audio, static/movie.
    """
    if request.method == "POST":
        # recursively go through all files in static and delete only the files
        for root, dirs, files in os.walk("file-server/static"):
            for file in files:
                os.remove(os.path.join(root, file))

        return jsonify({"message": "All files deleted."})


if __name__ == "__main__":
    app.run(debug=True)
