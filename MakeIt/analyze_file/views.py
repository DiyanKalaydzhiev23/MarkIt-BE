from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from analyze_file.actions import extract_text_from_pdf, video_detect_text
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


class AnalyzeVideo(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'video',
            openapi.IN_QUERY,
            type=openapi.TYPE_FILE,
        ),
    ])
    def post(self, request, *args, **kwargs):
        video_file = request.FILES.get('video')
        if not video_file:
            return Response({"error": "No video file provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response_data = video_detect_text(video_file)
            print("the res", response_data)
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
