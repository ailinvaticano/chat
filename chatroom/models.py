from django.db import models
from django.contrib.auth.models import User


class Chatbox(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_chatbox')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name="guest_chatbox")
    boxname = models.CharField(max_length=50, help_text="Ingrese un numbre para su box")

    def __str__(self):
        return self.boxname


class Message(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    chatbox = models.ForeignKey('Chatbox', on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return self.content[:50]

