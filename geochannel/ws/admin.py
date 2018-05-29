from django.contrib import admin

from .models import WebSocket


@admin.register(WebSocket)
class WebSocketAdmin(admin.ModelAdmin):
    readonly_fields = ('admin_key', 'connection_key')
