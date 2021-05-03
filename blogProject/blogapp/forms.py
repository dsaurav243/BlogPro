from django import forms
from .models import Comment

class EmailForm(forms.Form):
    name =  forms.CharField(max_length=50)
    sender = forms.EmailField(max_length=50)
    receiver = forms.EmailField(max_length=50)
    comments = forms.CharField(required=False,widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','body']
