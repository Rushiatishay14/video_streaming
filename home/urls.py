# urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("interview_room/", views.interview_room, name="interview_room"),
    path("check_face/", views.check_face, name="check_face"),
    path("send_offer/", views.send_offer, name="send_offer"),
    path("send_answer/", views.send_answer, name="send_answer"),
    path("send_ice_candidate/", views.send_ice_candidate, name="send_ice_candidate"),
    path("submit_answers/", views.submit_answers, name="submit_answers"),
    path("call/", views.call, name="call"),
    path("upload/", views.upload_video, name="upload_video"),
    path("get_question_audio/", views.get_question_audio, name="get_question_audio"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
