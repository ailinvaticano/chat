from django import forms
from .models import Chatbox, Message


class ChatBoxCreateForm(forms.ModelForm):
    class Meta:
        model = Chatbox
        fields = ['boxname', 'guest']


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']


class MessageInfoForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

