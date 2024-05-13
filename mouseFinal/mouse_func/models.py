from django.db import models


class MouseData(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    image = models.ImageField(upload_to='mouse_images/')
    created_at = models.DateTimeField(auto_now_add=True)
