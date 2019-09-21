from urllib import request

from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,  # users don't have to type this manually
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
        extension = url.rsplit('.', 1)[1].lower()

        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid extensions')

        return url

    def save(self,
             force_insert=False,
             force_update=False,
             commit=True):
        image_inst = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = f'{slugify(image_inst.title)}.{image_url.rsplit(".", 1)[1].lower()}'

        response = request.urlopen(image_url)
        image_inst.image.save(image_name,
                              ContentFile(response.read()),
                              save=False)

        if commit:
            image_inst.save()

        return image_inst
