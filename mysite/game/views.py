import os

from django.http import FileResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views import View
from mysite import settings


# Create your views here.
def game_view(request):
    response = render(request, 'PenguinGame/index.html')
    response["Cross-Origin-Opener-Policy"] = "same-origin"
    response["Cross-Origin-Resource-Policy"] = "cross-origin"
    response["Cross-Origin-Embedder-Policy"] = "require-corp"
    return response


class GameFileView(View):
    def get(self, request, filename):
        base_path = os.path.join(settings.BASE_DIR, 'static/game')
        file_path = os.path.join(base_path, filename)

        if os.path.exists(file_path):
            file = open(file_path, 'rb')

            response = FileResponse(file)
            response["Cross-Origin-Opener-Policy"] = "same-origin"
            response["Cross-Origin-Resource-Policy"] = "cross-origin"
            response["Cross-Origin-Embedder-Policy"] = "require-corp"

            return response
        else:
            return HttpResponseNotFound("File not found")
