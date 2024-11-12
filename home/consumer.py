from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .serializers import UserSerializers
from channels.generic.websocket import AsyncWebsocketConsumer

import json
import logging

logger = logging.getLogger(__name__)


class TestConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        self.room_name = "candidate_answers"
        self.room_group_name = f"candidate_answers_group"
        self.groups = []

    async def connect(self):
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.send_json({"status": "Connected successfully."})

    async def receive_json(self, content, **kwargs):
        await self.send_json({"message": "Received your JSON data", "data": content})

    async def send_json(self, content, close=False):
        await self.save_to_database(content)
        return await super().send_json(content, close)

    @database_sync_to_async
    def save_to_database(self, data):
        if data.get("message") is not None:
            data = data["data"]
            serializer = UserSerializers(data=data)
            if serializer.is_valid():
                instance = serializer.create_or_update_instance(
                    serializer.validated_data
                )
                print(serializer.data)
            print(serializer.errors)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await super().disconnect(code)


# class SignalingConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = "candidate_answers_videos"
#         self.room_group_name = f"room_{self.room_name}"
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)

#         # Handle end call event
#         if data.get('type') == 'end_call':
#             await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'end_call_message',
#                 'message': 'Call ended by one user',
#                 'initiator': data.get('initiator', False)
#             }
#         )

#         # Handle mute/unmute event
#         elif data.get('type') == 'mute_unmute':
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'mute_unmute_message',
#                     'message': f"User is {'muted' if data['muted'] else 'unmuted'}",
#                     'muted': data['muted']
#                 }
#             )

#         # Handle standard WebRTC signaling messages
#         else:
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'send_sdp',
#                     'message': data
#                 }
#             )

#     async def send_sdp(self, event):
#         message = event['message']
#         await self.send(text_data=json.dumps(message))

#     async def end_call_message(self, event):
#         # Notify clients that the call is ending
#         await self.send(text_data=json.dumps({
#             'type': 'end_call',
#             'message': event['message']
#         }))

#     async def mute_unmute_message(self, event):
#         # Notify clients that a user has muted/unmuted
#         await self.send(text_data=json.dumps({
#             'type': 'mute_unmute',
#             'message': event['message'],
#             'muted': event['muted']
#         }))

import json
from channels.generic.websocket import AsyncWebsocketConsumer


class InterviewConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"interview_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # Send a message to initiate screen sharing
        await self.send(text_data=json.dumps({"action": "start_screen_share"}))

    async def receive(self, text_data):
        data = json.loads(text_data)

        # After screen share is confirmed, ask to start camera
        if data.get("screen_share_confirmed"):
            await self.send(text_data=json.dumps({"action": "start_camera"}))

        # Broadcast SDP and ICE candidates to the group
        if data.get("sdp") or data.get("candidate"):
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "webrtc_message", "message": data}
            )

    async def webrtc_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps(message))

    async def notification(self, event):
        message = event["message"]
        await self.send(
            text_data=json.dumps({"action": "notification", "message": message})
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
