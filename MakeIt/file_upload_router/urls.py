from django.urls import path
from file_upload_router.views import FileUploadView, UserProfileMediaView, CreateProjectView

urlpatterns = [
    path('upload-file/', FileUploadView.as_view(), name='upload-file'),
    path('get-user-files/', UserProfileMediaView.as_view(), name='get-user-files'),
    path('projects/create/',CreateProjectView.as_view(), name='create-project'),
]
