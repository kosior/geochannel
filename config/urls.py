from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('', include('chat.urls')),
    path('ws/', include('ws.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
