import json
from channels.generic.websocket import AsyncWebsocketConsumer
from pynput.mouse import Listener as MouseListener
from django.core.files.base import ContentFile
import cv2
from .models import MouseData


class MouseDataConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mouse_listener = None

    async def connect(self):
        await self.accept()
        self.mouse_listener = MouseListener(on_move=self.on_mouse_move, on_click=self.on_mouse_click)
        self.mouse_listener.start()
        # await self.send(text_data=json.dumps({
        #     'type': 'image.capture.success',
        #     'message': 'Dummy message.',
        # }))

    async def disconnect(self, close_code):
        if self.mouse_listener:
            self.mouse_listener.stop()

    def on_mouse_move(self, x, y):
        text_data = {
            'type': 'mouse.move',
            'x': x,
            'y': y,
        }
        self.send(text_data=json.dumps(text_data))

    def on_mouse_click(self, x, y, button, pressed):
        if pressed and button == button.left:
            image_data = MouseDataConsumer.capture_image()
            image_name = 'example.jpg'
            image_file = ContentFile(image_data, name=image_name)
            mouse_data = MouseData.objects.create(x=x, y=y, image=None)
            mouse_data.image.save(image_name, image_file)
            mouse_data.save()
            text_data = {
                'type': 'image.capture.success',
                'message': 'Image captured successfully.',
            }
            self.send(text_data=json.dumps(text_data))

    @staticmethod
    def capture_image():
        webcam = cv2.VideoCapture(0)
        ret, frame = webcam.read()
        webcam.release()
        _, jpeg_image = cv2.imencode('.jpg', frame)
        return jpeg_image.tobytes()
