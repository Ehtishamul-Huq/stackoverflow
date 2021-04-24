from django.urls import path, include
from .views import QuestionAPI

urlpatterns = [
    path('questions/', QuestionAPI.as_view(), name="questions"),
]
