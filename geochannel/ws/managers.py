from django.db import models


class WebSocketManager(models.Manager):
    def get_with_permissions(self, uuid, token):
        try:
            ws = self.get(uuid=uuid)
        except self.model.DoesNotExist:
            return None
        else:
            ws.establish_permissions(token)
            return ws
