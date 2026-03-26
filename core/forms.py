from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Feedback


class RegisterForm(UserCreationForm):
    """Custom registration form with email field."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']



class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'What is your feedback about?'}),
            'message': forms.Textarea(attrs={'placeholder': 'Please share your thoughts...', 'rows': 5}),
        }
