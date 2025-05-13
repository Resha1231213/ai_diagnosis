from django import forms
from .models import UserRequest

class UserRequestForm(forms.ModelForm):
    file = forms.FileField(required=False)  # вот это убирает обязательность

    class Meta:
        model = UserRequest
        fields = ['full_name', 'email', 'file', 'question']