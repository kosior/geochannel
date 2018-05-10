from django.conf import settings
from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY})
