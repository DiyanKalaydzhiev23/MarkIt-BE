from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import views, status
from rest_framework.response import Response
from file_upload_router.models import Project
from helpers import get_summary_for_extracted_text
from summary_app.models import ProjectPrompts


class QueryProject(views.APIView):

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'prompt',
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'project_name',
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
        ),
    ])
    def post(self, request):
        prompt = request.data.get('prompt')
        project_name = request.data.get('project_name')
        old_conversations = request.data.get('old_conversations', [])

        try:
            project = Project.objects.get(project_name=project_name)
        except Project.DoesNotExist:
            return Response(
                {'error': 'Project not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        prompts = ProjectPrompts.objects.filter(project=project)
        result = list(f"In file: {el.file.file_path} {el.prompt}" for el in prompts)

        result = get_summary_for_extracted_text(result, prompt, old_conversations)

        return Response(
            {
                'result': result,
            },
            status=status.HTTP_200_OK
        )
