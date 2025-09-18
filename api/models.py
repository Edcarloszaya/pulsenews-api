from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class News(models.Model):

    CATEGORIA_CHOICES = [
        ("geral", "Geral"),
        ("esportes", "Esportes"),
        ("tecnologia", "Tecnologia"),
        ("negócios", "Negócios"),
    ]

    title = models.CharField(max_length=250)
    description = models.TextField()
    content = models.TextField()
    url = models.URLField(max_length=500)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    published_at = models.DateTimeField()
    category = models.CharField(
        max_length=20, default="geral", choices=CATEGORIA_CHOICES
    )
    source = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["published_at"]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["published_at"]),
        ]

    def __str__(self):
        return self.title

class ApiKey(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    api_key = models.CharField(max_length=64,unique=True)

    def __str__(self):
        return f'{self.user}'

