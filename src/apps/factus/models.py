from django.db import models

class AuthToken(models.Model):
    access_token = models.TextField(max_length=max)
    refresh_token = models.TextField(max_length=max)
    created_at = models.DateTimeField(auto_now_add=True)  # Para saber cuándo se guardó el token

    def __str__(self):
        return f"AuthToken {self.id} {self.access_token} {self.refresh_token}"