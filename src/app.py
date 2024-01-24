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

PORT = os.environ["PORT"]
app = Flask(__name__)
CORS(app)
PALM_API_KEY = os.environ["PALMAPI"]


@app.route("/", methods=["GET"])
def home():
    return "Hi"


@app.route("/text", methods=["POST"])
def text():
    """Send prompt to palm 2 API, get text. Use keywords to get images."""
    user_id = us.generate_uuid()
    us.generate_folder_structure(user_id)
    data = json.loads(request.data.decode("utf-8"))

    # Use dict.get() to check for missing keys
    keywords = data.get("keywords")
    if keywords is None:
        return jsonify({"error": "Missing keywords in request"}), 400

    txtr = data.get("text")
    if text is None:
        return jsonify({"error": "Missing text in request"}), 400

    img_urls = search_images(os.environ["PEXELSAPI"], keywords)
    download_images(img_urls, f"static/{user_id}/images")
    imgs = os.listdir(f"./static/{user_id}/images")
    txt = llm.generate_text(
        "Write a 1 minute info speech in plaintext for :" + txtr + "\n Only text, no links. Keep the language simple")
    return jsonify(
        {
            "user_id": user_id,
            "text": txt,
            "image_urls": [f"/static/{user_id}/images/{image}" for image in imgs],
        }
    )

# curl -X POST -H "Content-Type: application/json" -d '{"keywords": ["cat", "dog"], "text": "cats and dogs"}' http://localhost:5000/text


@app.route("/edittext", methods=["POST"])
def edittext():
    """
    Takes in a text, generates a voiceover, and creates a video with the voiceover.
    Returns the URL of the generated video.
    """
    data = json.loads(request.data.decode("utf-8"))

    # Use dict.get() to check for missing keys
    edit_text = data.get("text")
    if edit_text is None:
        return jsonify({"error": "Missing text in request"}), 400

    user_id = data.get("user_id")
    if user_id is None:
        return jsonify({"error": "Missing user_id in request"}), 400

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

# curl -X POST -H "Content-Type: application/json" -d '{"text": "cats and dogs", "user_id": "test"}' http://localhost:5000/edittext


@app.route("/images", methods=["POST"])
def images():
    """
    Takes user_id from json body and returns the urls of the images (from local storage).
    If it doesn't exist returns an error message.
    """
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
    json_data = json.loads(request.data.decode("utf-8"))
    user_id = json_data["user_id"]
    if os.path.exists(
        f"./static/{user_id}/movie/output_video_with_audio.mp4"
    ):
        return jsonify(
            {
                "user_id": user_id,
                "video_url": f"/static/{user_id}/movie/output_video_with_audio.mp4",
            }
        )
    else:
        return jsonify({"error": "Video not found."})


if __name__ == "__main__":
    app.run(debug=True)
