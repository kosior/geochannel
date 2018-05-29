from django.urls import path

from .views import CreateWebSocket, SendContent


app_name = 'ws'

urlpatterns = [
    path('', CreateWebSocket.as_view(), name='create'),
    path('<uuid:uuid>/', SendContent.as_view(), name='send'),
]
