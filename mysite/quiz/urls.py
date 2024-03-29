from django.urls import path
from . import views

#Author: Tom

app_name = "quiz"
urlpatterns = [
        path("attempt/", views.QuizAttempt, name="QuizAttempt"),
        path("result/", views.QuizResult, name="QuizResult"),
        path("result/display", views.QuizResultDisplay, name="QuizResultDisplay")
]