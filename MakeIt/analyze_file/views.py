import cloudinary.uploader
import os

from django.core.files.base import ContentFile
from moviepy.editor import VideoFileClip

from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response

from MakeIt import settings
from analyze_file.actions import extract_text_from_pdf, analyze_audio
from file_upload_router.models import UserProfileMedia
from helpers import get_summary_for_extracted_text
from summary_app.actions import save_project_prompt


class AnalyzePdf(APIView):

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'file_path',
            openapi.IN_QUERY,
            type=openapi.TYPE_FILE,
            description="full path example: project_name/path/filename.extension"
        )
    ])
    def post(self, request, *args, **kwargs):
        user = request.user
        file_path = request.data.get('file_path')

        data: list = extract_text_from_pdf(file_path, user.username)
        end_result = get_summary_for_extracted_text(data)
        project_name = file_path.split('/')[0]
        file = UserProfileMedia.objects.get(file_path=file_path)

        save_project_prompt(end_result, project_name, file)

        return Response(
            {"analysis": end_result},
            status=status.HTTP_201_CREATED
        )


class AnalyzeAudio(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'file',
            openapi.IN_QUERY,
            type=openapi.TYPE_FILE,
        ),
        openapi.Parameter(
            'file_path',
            openapi.IN_QUERY,
            type=openapi.TYPE_FILE,
            description="full path example: project_name/path/filename.extension"
        )
    ])
    def post(self, request, *args, **kwargs):
        # Configure Cloudinary with the credentials from Django settings
        cloudinary.config(
            cloud_name=settings.CLOUDINARY['cloud_name'],
            api_key=settings.CLOUDINARY['api_key'],
            api_secret=settings.CLOUDINARY['api_secret'],
        )

        audio_file = request.FILES.get('file')
        if not audio_file:
            return Response({"error": "Audio file is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            upload_result = cloudinary.uploader.upload(
                audio_file,
                resource_type='auto',
                folder='audio_uploads',
            )
            overview = analyze_audio("https://" + "".join(upload_result['url'].split("://")[1:]))

            return Response({"overview": overview}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AnalyzeVideo(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'file',
            openapi.IN_QUERY,
            type=openapi.TYPE_FILE,
        )
    ])
    def post(self, request, *args, **kwargs):
        video_file = request.FILES.get('file')
        file_path = request.data.get('file_path')

        cloudinary.config(
            cloud_name=settings.CLOUDINARY['cloud_name'],
            api_key=settings.CLOUDINARY['api_key'],
            api_secret=settings.CLOUDINARY['api_secret'],
        )

        if not video_file:
            return Response({"error": "No video file provided."}, status=status.HTTP_400_BAD_REQUEST)

        video = VideoFileClip(video_file.temporary_file_path())
        audio = video.audio
        temp_audio_path = "temp_audio.mp3"
        audio.write_audiofile(temp_audio_path)
        video.close()

        with open(temp_audio_path, 'rb') as f:
            audio_content = ContentFile(f.read(), name="output_audio.mp3")
            upload_result = cloudinary.uploader.upload(
                audio_content,
                resource_type='auto',
                folder='audio_uploads',
            )
            overview = analyze_audio("https://" + "".join(upload_result['url'].split("://")[1:]))

            project_name = file_path.split('/')[0]
            file = UserProfileMedia.objects.get(file_path=file_path)
            save_project_prompt(overview, project_name, file)

        os.remove(temp_audio_path)

        return Response({"overview": overview}, status=status.HTTP_200_OK)