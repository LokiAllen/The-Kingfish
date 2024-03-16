from django.apps import AppConfig

#Author: Tom

class QuizConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "quiz"

    #Import custom template filter from folder.
    def ready(self):
        import quiz.templatetags.tfilters
