from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class EducationalResource(models.Model):
    RESOURCE_TYPES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('guide', 'Guide'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES,default='article')
    file = models.FileField(upload_to='resources/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title