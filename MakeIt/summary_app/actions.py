from django.core.exceptions import ObjectDoesNotExist
from file_upload_router.models import Project
from summary_app.models import ProjectPrompts


def save_project_prompt(prompt_text, project_name, file):
    try:
        project = Project.objects.get(project_name=project_name)
    except ObjectDoesNotExist:
        print(f"No project found with the name '{project_name}'. Prompt not saved.")
        return None

    # Create and save the new ProjectPrompts instance with the found project
    project_prompt = ProjectPrompts(prompt=prompt_text, project=project, file=file)
    project_prompt.save()

    return project_prompt
