from .models import FileModel
from django import forms

class FileForm(forms.ModelForm):

    class Meta:
        model = FileModel
        fields = ["file"]