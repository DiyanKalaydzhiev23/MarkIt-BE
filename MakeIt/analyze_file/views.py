import uuid

from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from google.cloud import storage
from google.cloud import videointelligence
from rest_framework.response import Response
from analyze_file.actions import extract_text_from_pdf
from helpers import get_summary_for_extracted_text


class AnalyzePdf(APIView):

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'filename',
            openapi.IN_QUERY,
            type=openapi.TYPE_FILE,
        ),
        openapi.Parameter(
            'extension',
            openapi.IN_QUERY,
            type=openapi.TYPE_FILE,
        ),
    ])
    def post(self, request, *args, **kwargs):
        user = request.user
        filename = request.data.get('filename')
        extension = request.data.get('extension')

        data: list = extract_text_from_pdf(filename, extension, user.username)
        end_result = get_summary_for_extracted_text(data)

        return Response(
            {"analysis": end_result},
            status=status.HTTP_201_CREATED
        )


class AnalyzeVideo(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'video',
            openapi.IN_QUERY,
            type=openapi.TYPE_FILE,
        ),
    ])
    def post(self, request, *args, **kwargs):
        # Assuming the video is sent as a file in a form-data request
        video_file = request.FILES.get('video')
        if not video_file:
            return Response({"error": "No video file provided."}, status=400)

        # Initialize Google Cloud Storage client
        storage_client = storage.Client()
        bucket_name = "your-gcs-bucket-name"
        bucket = storage_client.bucket(bucket_name)

        # Generate a unique filename for GCS upload
        gcs_filename = f"uploads/{uuid.uuid4()}.mp4"
        blob = bucket.blob(gcs_filename)

        # Upload the video file to GCS
        blob.upload_from_file(video_file, content_type=video_file.content_type)

        # Now the video is in GCS, and we have its URI
        gcs_uri = f"gs://{bucket_name}/{gcs_filename}"

        # Call the Video Intelligence API with the GCS URI
        video_client = videointelligence.VideoIntelligenceServiceClient()
        features = [videointelligence.Feature.SPEECH_TRANSCRIPTION]
        operation = video_client.annotate_video(input_uri=gcs_uri, features=features)
        result = operation.result(timeout=180)

        # Process the result...

        print("the result", result)

        # Optionally, delete the video from GCS after processing
        blob.delete()

        return Response({"message": "Video processed successfully"})
