from django import forms
from .models import Story


class StoryForm(forms.ModelForm):

    class Meta:
        model = Story
        fields = ["image", "caption"]

        widgets = {
            "caption": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write a caption..."
                }
            )
        }