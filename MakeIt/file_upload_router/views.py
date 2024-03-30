from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from auth_app.models import Profile
from file_upload_router.actions import upload_file_to_bucket
from file_upload_router.models import UserProfileMedia, Project
from file_upload_router.serializers import UserProfileMediaSerializer, ProjectSerializer


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'file',
            openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            required=True,
        ),
        openapi.Parameter(
            'project_name',
            openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ])
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        project_name = request.data.get('project_name')

        if not file_obj or not project_name:
            return Response({"error": "File and project name are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        if str(file_obj).count('.') > 1:
            return Response(
                {"error": "Cannot have more than one '.' in file name"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the project exists for the given user's profile
        profile = user.profile  # Assuming a one-to-one relationship with Profile
        project, created = Project.objects.get_or_create(
            project_name=project_name,
            defaults={'profile': profile}
        )

        project_name = request.data.get('project_name')
        project_path = request.data.get('project_path')

        if not project_name or not project_path:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        filename, extension = str(file_obj).rsplit('.', 1)
        file_path = f"{project_name}/{project_path}/{filename}.{extension}"
        upload_response = upload_file_to_bucket(file_obj, file_path, user.username)

        if not upload_response.ok:
            return Response(
                {"error": upload_response.reason},
                status=upload_response.status
            )

        # Save the file information to the database linked with the found or created project
        UserProfileMedia.objects.create(
            file_path=filename,
            extension=extension,
            project=project
        )

        return Response(
            {
                "message": "File uploaded and saved successfully",
                "project": project_name,
                "filename": filename,
                "extension": extension,
            },
            status=status.HTTP_201_CREATED
        )


class UserProfileMediaView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all user profile media items, organized by projects.",
        responses={
            200: 'A dictionary with projects as keys and lists of media items as values.',
            404: 'User does not have a profile.'
        }
    )
    def get(self, request, *args, **kwargs):
        user = request.user

        if not hasattr(user, 'profile'):
            return Response({"error": "User does not have a profile."}, status=status.HTTP_404_NOT_FOUND)

        # Initialize a dictionary to hold the response data
        projects_files = {}

        # Iterate over projects associated with the user's profile
        for project in Project.objects.filter(profile=user.profile):
            media_items = UserProfileMedia.objects.filter(project=project)
            serializer = UserProfileMediaSerializer(media_items, many=True)
            projects_files[project.project_name] = serializer.data

        if not projects_files:
            return Response({"message": "No projects or media items found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(projects_files, status=status.HTTP_200_OK)


class CreateProjectView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'project_name',
            openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            required=True,
        ),
    ])
    def post(self, request, *args, **kwargs):
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)

        # Make a mutable copy of request.data
        mutable_data = request.data.copy()
        mutable_data['profile'] = profile.user_id

        serializer = ProjectSerializer(data=mutable_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
