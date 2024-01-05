import os
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from imgget import search_images, download_images
import voiceovergen as vo
import moviegen as mg
import llm_req as llm
import userstuff as us

load_dotenv()

PORT = os.environ["FILE_SERVER_PORT"]
app = Flask(__name__)
CORS(app)
PALM_API_KEY = os.environ["PALMAPI"]


@app.route("/text", methods=["POST"])
def text():
    """Send prompt to palm 2 API, get text. Use keywords to get images."""
    if request.method == "POST":
        user_id = us.generate_uuid()
        us.generate_folder_structure(user_id)
        data = json.loads(request.data.decode("utf-8"))
        keywords = data["keywords"]
        img_urls = search_images(os.environ["PEXELSAPI"], keywords)
        download_images(img_urls, f"static/{user_id}/images")
        imgs = os.listdir(f"./static/{user_id}/images")
        txt = llm.generate_text(
            "Write a 1 minute info speech in plaintext for :" + data["text"]
        )
        return jsonify(
            {
                "user_id": user_id,
                "text": txt,
                "image_urls": [f"/static/{user_id}/images/{image}" for image in imgs],
            }
        )


@app.route("/edittext", methods=["POST"])
def edittext():
    """
    Takes in a text, generates a voiceover, and creates a video with the voiceover.
    Returns the URL of the generated video.
    """
    if request.method == "POST":
        data = json.loads(request.data.decode("utf-8"))
        edit_text = data["text"]
        user_id = data["user_id"]
        vo_url = vo.generate_voiceover(
            str(edit_text), f"./static/{user_id}/audio/output_voiceover.mp3"
        )
        mg.create_video(
            vo_url,
            image_folder=f"./static/{user_id}/images",
            output_file=f"./static/{user_id}/movie/output_video_with_audio.mp4",
        )
        return jsonify(
            {"video_url": f"/static/{user_id}/movie/output_video_with_audio.mp4"}
        )


@app.route("/images", methods=["POST", "GET"])
def images():
    """
    Takes user_id from json body and returns the urls of the images (from local storage).
    If it doesn't exist returns an error message.
    """
    if request.method == "POST":
        json_data = json.loads(request.data.decode("utf-8"))
        user_id = json_data["user_id"]
        if os.path.exists(f"file-server/static/{user_id}/images"):
            imgs = os.listdir(f"./static/{user_id}/images")
            return jsonify(
                {
                    "user_id": user_id,
                    "image_urls": [
                        f"/static/{user_id}/images/{image}" for image in imgs
                    ],
                }
            )
        else:
            return jsonify({"error": "Images not found."})


@app.route("/voiceover", methods=["POST"])
def voiceover():
    """
    Takes user_id from json body and returns the url of the voiceover (from local storage).
    If it doesn't exist returns an error message.
    """
    if request.method == "POST":
        json_data = json.loads(request.data.decode("utf-8"))
        user_id = json_data["user_id"]
        if os.path.exists(f"file-server/static/{user_id}/audio/output_voiceover.mp3"):
            return jsonify(
                {
                    "user_id": user_id,
                    "voiceover_url": f"/static/{user_id}/audio/output_voiceover.mp3",
                }
            )
        else:
            return jsonify({"error": "Voiceover not found."})


@app.route("/movie", methods=["POST"])
def movie():
    """
    Takes user_id from json body and returns the url of the video (from local storage). If it doesn't exist returns an error message.
    """
    if request.method == "POST":
        json_data = json.loads(request.data.decode("utf-8"))
        user_id = json_data["user_id"]
        if os.path.exists(
            f"file-server/static/{user_id}/movie/output_video_with_audio.mp4"
        ):
            return jsonify(
                {
                    "user_id": user_id,
                    "video_url": f"/static/{user_id}/movie/output_video_with_audio.mp4",
                }
            )
        else:
            return jsonify({"error": "Video not found."})



@app.route("/reset", methods=["POST"])
def reset():
    """
    Deletes all files in static/images, static/audio, static/movie.
    """
    data = json.loads(request.data.decode("utf-8"))
    user_id = data["user_id"]
    if request.method == "POST":
        # recursively go through all files in static and delete only the files
        for root, dirs, files in os.walk(f"./static/{user_id}"):
            for file in files:
                os.remove(os.path.join(root, file))
        us.remove_folder_structure(user_id)

        return jsonify({"message": "All files deleted.", "user_id": user_id})


if __name__ == "__main__":
    app.run(debug=True)
