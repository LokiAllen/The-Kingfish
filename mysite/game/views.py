from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    response = render(request, 'PenguinGame/index.html')
    response["Cross-Origin-Opener-Policy"] = "same-origin"
    #response["Cross-Origin-Embedder-Policy"] = "require-corp"
    response["Cross-Origin-Resource-Policy"] = "cross-origin"
    response["Cross-Origin-Embedder-Policy"] = "require-corp"

    # Allow cross-origin requests for worker files
    response["Cross-Origin-Resource-Policy"] = "cross-origin"

    return response

# Create your views here.
