from django import forms
from .models import Message


class MessageForm(forms.ModelForm):

    class Meta:

        model = Message

        fields = ["message"]

        widgets = {

            "message": forms.TextInput(

                attrs={

                    "class": "form-control rounded-pill",

                    "placeholder": "Type a message...",

                    "autocomplete": "off",

                    "id": "id_message",

                }

            )

        }