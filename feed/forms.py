from django import forms
from feed.models import Comment, Post

class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True

class MultipleFilesField(forms.FileField):
    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(x, initial) for x in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'multiple': True, "class": "form-control"}))
        super().__init__(*args, **kwargs)


class PostForm(forms.ModelForm):
    images = MultipleFilesField(
        required=True,
        label='Choose images',
    )

    class Meta:
        model = Post
        fields = ['description']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}),
        }
