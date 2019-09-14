from django import forms


class EmailPostForm(forms.Form):
    """Each widget has its own validation rule (e.g. <textarea>, <input>)
    """
    name = forms.CharField(max_length=25)
    email_from = forms.EmailField()
    email_to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)
