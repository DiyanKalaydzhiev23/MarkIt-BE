from django.urls import path
from file_upload_router.views import FileUploadView

urlpatterns = [
    path('upload-file/', FileUploadView.as_view(), name='upload-file'),
]
