from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
import os
import speech_recognition as sr
from pydub import AudioSegment
import io
import cv2
import numpy as np
from gtts import gTTS

questions = [
    "What is your name?",
    "What is your experience?",
    "Why do you want this job?",
    # Add more questions as needed
]


def detect_face(frame):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return faces


def process_frame(frame):
    faces = detect_face(frame)
    if len(faces) == 0:
        return False, "No face detected"
    else:
        return True, "Face detected"


@csrf_exempt
def check_face(request):
    if request.method == "POST":
        # Verify image data is present
        if "image" not in request.FILES:
            return JsonResponse(
                {"status": "error", "message": "No image provided"}, status=400
            )

        # Read and decode the image data
        image_data = request.FILES["image"].read()
        np_image = np.frombuffer(image_data, np.uint8)

        # Attempt to decode the image
        frame = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
        if frame is None:
            return JsonResponse(
                {"status": "error", "message": "Failed to decode image"}
            )

        # Process the frame for face detection
        is_face_detected, message = process_frame(frame)

        # Send notification if no face detected
        if not is_face_detected:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "candidate_answers_videos",  # Replace with your channel name
                {"type": "notification", "message": message},
            )
            return JsonResponse({"status": "error", "message": message})

        return JsonResponse({"status": "success", "message": message})

    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=405
    )


def interview_room(request):
    return render(request, "videos.html", {"room_name": "candidate_answers_videos"})


@csrf_exempt
def send_offer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            data["room_name"],
            {"type": "send.sdp", "sdp": data["sdp"], "sender": data["sender"]},
        )
        return JsonResponse({"status": "ok"})


@csrf_exempt
def send_answer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            data["room_name"],
            {"type": "send.sdp", "sdp": data["sdp"], "sender": data["sender"]},
        )
        return JsonResponse({"status": "ok"})


@csrf_exempt
def send_ice_candidate(request):
    if request.method == "POST":
        data = json.loads(request.body)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            data["room_name"],
            {
                "type": "send.ice_candidate",
                "candidate": data["candidate"],
                "sender": data["sender"],
            },
        )
        return JsonResponse({"status": "ok"})


@csrf_exempt
def submit_answers(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        if not os.path.exists("data"):
            os.makedirs("data")
        with open("data/answers.json", "w") as f:
            json.dump(data, f, indent=4)
        return JsonResponse(
            {"status": "success", "message": "Confirmation data received and stored."}
        )

        # Process the answers as needed
        # For example, save them to the database
        # For now, we'll just return the received data

        return JsonResponse({"status": "success", "answers": answers})
    else:
        return JsonResponse(
            {"status": "error", "message": "Invalid request method"}, status=405
        )


def call(request):
    return render(request, "videos.html")


@csrf_exempt
def upload_video(request):
    if request.method == "POST":
        if "camera_video" in request.FILES:
            video_file = request.FILES["camera_video"]
            file_name = f"{os.path.splitext(video_file.name)[0]}.mp4"
            path = default_storage.save(
                "videos/" + file_name, ContentFile(video_file.read())
            )
            return JsonResponse({"status": "success", "path": path})
        elif "screen_video" in request.FILES:
            video_file = request.FILES["screen_video"]
            file_name = f"{os.path.splitext(video_file.name)[0]}.mp4"
            path = default_storage.save(
                "videos/" + file_name, ContentFile(video_file.read())
            )
            return JsonResponse({"status": "success", "path": path})
        else:
            return JsonResponse(
                {"status": "error", "message": "No video file found"}, status=400
            )
    return JsonResponse({"status": "error"}, status=400)


@csrf_exempt
def get_question_audio(request):
    if request.method == "POST":
        data = json.loads(request.body)
        question_index = data.get("question_index")

        if (
            question_index is None
            or question_index < 0
            or question_index >= len(questions)
        ):
            return JsonResponse(
                {"status": "error", "message": "Invalid question index"}, status=400
            )

        question = questions[question_index]

        # Convert text to speech
        tts = gTTS(text=question, lang="en")
        audio_data = io.BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)

        # Return the audio data as a response
        response = JsonResponse({"status": "success", "question": question})
        response["Content-Disposition"] = 'attachment; filename="question.mp3"'
        response["Content-Type"] = "audio/mpeg"
        response.content = audio_data.read()

        return response

    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=405
    )
