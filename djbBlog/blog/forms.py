from django import forms

from .models import Comment


class EmailPostForm(forms.Form):
    """Each widget has its own validation rule (e.g. <textarea>, <input>)
    """
    name = forms.CharField(max_length=25)
    email_from = forms.EmailField()
    email_to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    """Since this form is mostly based on the `Comment` model,
    we don't have to write every fields again, just name what we need is enough.
    """

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
