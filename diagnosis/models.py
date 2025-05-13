from django.db import models

class UserRequest(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    file = models.FileField(upload_to='uploads/')
    question = models.TextField()
    ai_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})"