from django.urls import path
from analyze_file.views import AnalyzePdf, AnalyzeVideo

urlpatterns = [
    path('analyze-pdf/', AnalyzePdf.as_view(), name='analyze-pdf'),
    path('analyze-video/', AnalyzeVideo.as_view(), name="analyze-video"),
]
