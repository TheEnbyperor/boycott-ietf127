from django import forms
from . import models


class SignatureForm(forms.ModelForm):
    public = forms.ChoiceField(choices=(
        (True, "Yes"),
        (False, "No"),
    ))

    class Meta:
        model = models.Signature
        fields = (
            "name", "affiliation", "email", "situation", "public"
        )
