from django import forms
from django.contrib.auth.models import User

from accounts.models import UserProfile

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
