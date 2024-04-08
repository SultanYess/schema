import cv2
import uuid
import json
import base64
import numpy as np
import face_recognition as fr


from PIL import Image
from io import BytesIO
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from apps.fr.models import OriginalImage, RecognizedFace
from apps.organizations.models import EmployeeEvent, Employee
from apps.organizations import EmployeeEventTypes
from apps.organizations.models import Event


from django.core.files.base import ContentFile

class RecognizedFaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecognizedFace
        fields = (
            "id",
            "face_image",
            "vector",
        )


class EmployeeEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeEvent
        fields = (
            "id",
            "employee",
            "event_type",
            "event_start_date",
            "event_note",
            "original_image",
        )


class OriginalImageSerializer(serializers.ModelSerializer):
    """Сериализатор FaceID"""
    recognized_faces = RecognizedFaceSerializer(many=True, read_only=True)
    class Meta:
        model = OriginalImage
        fields = (
            "id",
            "original_image",
            "created_by",
            "recognized_faces",
        )

    def create(self, validated_data):
        created_by = validated_data.pop('created_by')
        original_image_file = validated_data.pop(
            'original_image')  # Assuming 'original_image' is the field storing the image file

        try:
            employee = Employee.objects.get(user=created_by)
        except ObjectDoesNotExist:
            employee = Employee.objects.create(user=created_by)

        original_image = OriginalImage.objects.create(created_by=created_by)

        # Open the image file from the model instance
        pil_image = Image.open(original_image_file).convert("RGB")
        with BytesIO() as byte_image:
            pil_image.save(byte_image, format='JPEG')
            image_bytes = byte_image.getvalue()

        numpy_image = np.array(pil_image)
        face_locations = fr.face_locations(numpy_image)
        face_encodings = fr.face_encodings(numpy_image, face_locations)
        for fl, encoding in zip(face_locations, face_encodings):
            top, right, bottom, left = fl
            face_image = numpy_image[top:bottom, left:right]
            _, buffer = cv2.imencode(
                ".png", cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR)
            )
            face_image_base64 = base64.b64encode(buffer).decode("utf-8")
            temp_image = BytesIO()
            Image.fromarray(face_image).save(temp_image, format="JPEG")

            original_image_instance = OriginalImage.objects.create(
                original_image=ContentFile(
                    image_bytes,
                    name=f"face_image_{uuid.uuid4()}.jpg",
                ),
                created_by=created_by,
            )
            vector_list = encoding.tolist()
            vector_json = json.dumps(vector_list)
            recognized_face = RecognizedFace.objects.create(
                original_image=original_image_instance,
                face_image=face_image_base64,
                vector=vector_json
            )

        last_events = EmployeeEvent.objects.filter(event_type__in=["coming", "leaving"]).order_by("-created_at")[:1]

        if last_events.exists():
            last_event = last_events[0]
            if last_event.event_type == "coming":
                employee_event=EmployeeEvent.objects.create(
                    employee=employee,
                    event_type=EmployeeEventTypes.LEAVING,
                    event_note='',
                    event_start_date=datetime.now()
                )
            else:
                employee_event=EmployeeEvent.objects.create(
                    employee=employee,
                    event_type=EmployeeEventTypes.COMING,
                    event_note='',
                    event_start_date=datetime.now()
                )
        else:
            employee_event=EmployeeEvent.objects.create(
                employee=employee,
                event_type=EmployeeEventTypes.COMING,
                event_note='',
                event_start_date=datetime.now()
            )
        Event.objects.create(
            employee=employee,
            recognized_face=recognized_face,
            employee_event=employee_event,
        )
        return original_image
