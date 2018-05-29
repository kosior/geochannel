import binascii
import os
import uuid

from django.db import models
from model_utils.models import TimeStampedModel

from .managers import WebSocketManager


class WebSocket(TimeStampedModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin_key = models.CharField(max_length=40, unique=True, editable=False)
    connection_key = models.CharField(max_length=40, unique=True, blank=True, null=True, editable=False)
    open_connection = models.BooleanField(default=False)
    open_sending = models.BooleanField(default=False)

    connect_permission = None
    send_permission = None

    objects = WebSocketManager()

    def __str__(self):
        return str(self.uuid)

    def save(self, *args, **kwargs):
        if not self.admin_key:
            self.admin_key = self.generate_key()

        if not self.connection_key and not self.open_connection:
            self.connection_key = self.generate_key()

        super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    @property
    def http_url(self):
        return 'https://'

    @property
    def ws_url(self):
        return 'wss://'

    def _get_permissions(self, token):
        if token == self.admin_key:
            return True, True

        if self.open_connection or (token and token == self.connection_key):
            return True, self.open_sending

        return False, False

    def establish_permissions(self, token):
        self.connect_permission, self.send_permission = self._get_permissions(token)
