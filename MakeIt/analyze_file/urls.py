from django.urls import path
from analyze_file.views import AnalyzePdf

urlpatterns = [
    path('analyze-pdf/', AnalyzePdf.as_view(), name='analyze-pdf'),
]
