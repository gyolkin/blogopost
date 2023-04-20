from django import forms

from .models import Comment, Post
from users.models import Profile


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'group', 'image')
        help_texts = {
            'text': 'Допускается использование markdown'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(
                attrs={'rows': 2, 'cols': 40}
            )
        }


class ProfileEdit(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'avatar')
