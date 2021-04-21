from django.urls import path, include
from .views import QuestionAPI, LatestView

urlpatterns = [
    path('latest/', LatestView.as_view(), name="latest"),
    path('questions/', QuestionAPI.as_view(), name="questions"),
]
