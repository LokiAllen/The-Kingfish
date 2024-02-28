from django.urls import path
from . import views


app_name = "quiz"
urlpatterns = [
        path("attempt/", views.QuizAttempt, name="QuizAttempt"),
        path("result/", views.QuizResult, name="QuizResult")
]