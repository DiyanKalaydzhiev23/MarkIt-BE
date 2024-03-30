from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from file_upload_router.actions import upload_file_to_bucket
from file_upload_router.models import UserProfileMedia
from file_upload_router.serializers import UserProfileMediaSerializer


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description="Retrieve all user profile media items.",
        responses={
            200: UserProfileMediaSerializer(many=True),
            404: 'User does not have a profile.'
        }
    )
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "File is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        # Validate file name
        if str(file_obj).count('.') > 1:
            return Response(
                {"error": "Cannot have more than one '.' in file name"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Splitting filename and extension
        filename, extension = str(file_obj).rsplit('.', 1)
        upload_response = upload_file_to_bucket(file_obj, filename, extension, user.username)

        # Assuming upload_file_to_bucket returns a response object with a 'ok' attribute
        if not upload_response.ok:
            return Response(
                {"error": upload_response.reason},
                status=upload_response.status
            )

        # Save the file information to the database
        profile = user.profile  # Assuming a one-to-one relationship with Profile
        UserProfileMedia.objects.create(
            file_path=filename,
            extension=extension,
            profile=profile
        )

        return Response(
            {
                "message": "File uploaded and saved successfully",
                "filename": filename,
                "extension": extension,
            },
            status=status.HTTP_201_CREATED
        )


class UserProfileMediaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not hasattr(user, 'profile'):
            return Response({"error": "User does not have a profile."}, status=status.HTTP_404_NOT_FOUND)

        media_items = UserProfileMedia.objects.filter(profile=user.profile)
        serializer = UserProfileMediaSerializer(media_items, many=True)

        print(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

