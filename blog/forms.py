from django import forms
from django.forms import fields, widgets
from .models import Post, Comment
#https://docs.djangoproject.com/en/4.2/ref/forms/widgets/
class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control custom-text', 'cols': '40', 'rows': '4'}), label='')
    class Meta:
        model = Comment
        fields = ['body',]