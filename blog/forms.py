from django import forms
from . import models

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = models.Comment
        exclude = ['post']
        labels = {
            "username" : "Your name",
            "user_email": "Your email",
            "text" : "Your comment"
        }

