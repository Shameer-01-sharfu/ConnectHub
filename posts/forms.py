from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = [
            "caption",
            "image",
        ]

        widgets = {

            "caption": forms.Textarea(

                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "What's on your mind?"
                }

            ),

            "image": forms.FileInput(

                attrs={
                    "class": "form-control"
                }

            ),

        }