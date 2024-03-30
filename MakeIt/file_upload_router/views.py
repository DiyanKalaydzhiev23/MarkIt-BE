from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from file_upload_router.actions import upload_file_to_bucket


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'file',
            openapi.IN_QUERY,
            type=openapi.TYPE_FILE,
        ),
    ])
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES['file']
        user = request.user

        if str(file_obj).count('.') > 1:
            return Response(
                {"error": "Cannot have more than one . in file name"},
                status=status.HTTP_400_BAD_REQUEST
            )

        filename, extension = str(file_obj).split('.')
        upload_response = upload_file_to_bucket(file_obj, filename, extension, user.username)

        if not upload_response.ok:
            return Response(
                {"error": upload_response.reason},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "filename": filename,
                "extension": extension,
            },
            status=status.HTTP_201_CREATED
        )
