from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from analyze_file.actions import extract_text_from_pdf, video_detect_text
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
        video_file = request.FILES.get('video')
        if not video_file:
            return Response({"error": "No video file provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response_data = video_detect_text(video_file)
            print("the res", response_data)
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
