from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import time
from .utils import llm_req


@csrf_exempt
def index(request):
    timestamp = time.time()
    client_ip = request.META["REMOTE_ADDR"]

    if request.method == "POST":
        json_data = json.loads(request.body.decode("utf-8"))
        text = json_data["text"]
        text = llm_req.generate_text("Write a long paragraph voiceover about " + text)[
            "output"
        ]
        return JsonResponse({"output": text})
    else:
        return JsonResponse(
            {"text": "Hello, World!", "timestamp": str(timestamp), "ip": str(client_ip)}
        )
