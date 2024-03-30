from django.urls import path

from summary_app.views import QueryProject

urlpatterns = [
    path('query-project/', QueryProject.as_view(), name='query-project'),
]
