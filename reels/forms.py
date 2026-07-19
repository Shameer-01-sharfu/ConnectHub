from django import forms
from .models import Reel, ReelComment


class ReelForm(forms.ModelForm):

    class Meta:

        model = Reel

        fields = [
            "caption",
            "video"
        ]


class ReelCommentForm(forms.ModelForm):

    class Meta:

        model = ReelComment

        fields = [
            "comment"
        ]

        widgets = {
            "comment": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write a comment..."
                }
            )
        }