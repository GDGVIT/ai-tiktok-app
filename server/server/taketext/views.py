import json
import asyncio
from django.http import JsonResponse

# Remove unused import statement
from django.views.decorators.csrf import csrf_exempt

from .utils import llm_req, gen_voiceover, image_get
import time


from django.views.decorators.csrf import csrf_exempt
import requests
import re


@csrf_exempt
async def index(request):
    """
    index that handles the initial script generation
    """
    timestamp = time.time()
    client_ip = request.META["REMOTE_ADDR"]


    if request.method == "POST":
        json_data = json.loads(request.body.decode("utf-8"))
        text = json_data["text"]
        keywords = text.split(" ")
        # Make a request to localhost:5000/images
        # This will return a list of image URLs

        # Get the image URLs
        image_urls = requests.post("http://localhost:5000/images", json={"keywords": keywords}).json()["image_urls"]
        text = llm_req.generate_text("Write a long paragraph voiceover about " + text) # This makes a call to the API and generates the text
        # Remove regex anything within ** **
        text = re.sub(r"\*\*.*?\*\*", "", text)
        return JsonResponse({"output": text})
    else:
        return JsonResponse(
            {"text": "Hello, World!", "timestamp": str(timestamp), "ip": str(client_ip)}
        )

@csrf_exempt
def generate_voiceover(request):
    # First, handle the text and store it in some file
    if request.method == "POST":
        json_data = json.loads(request.body.decode("utf-8"))
        text = json_data["text"]

        # Write the text to a file (you may want to use a more unique filename)
        with open("text.txt", "w", encoding="utf-8") as f:
            f.write(text)

        # Define an asynchronous function to generate the voiceover

        # You can also return any other data if needed

        # Start the asynchronous task
        gen_voiceover.generate_voiceover(text)
        return JsonResponse({"output": text, "status": "ok"})


@csrf_exempt
def test(request):
    return JsonResponse({"output": "test"})
