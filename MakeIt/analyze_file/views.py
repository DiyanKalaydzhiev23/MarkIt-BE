from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
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

        get_summary_for_extracted_text(data)

        return Response(status=status.HTTP_201_CREATED)
