from django import forms
from .models import Leader, Profile, Tag


class LeaderForm(forms.ModelForm):
    class Meta:
        model = Leader
        exclude = ['post_date', 'user', ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        exclude = ['user', ]

class RateForm(forms.Form):
    leadership=forms.IntegerField(
        max_value=10,
        min_value=0
    )
    publicity=forms.IntegerField(
        max_value=10,
        min_value=0
    )
    integrity=forms.IntegerField(
        max_value=10,
        min_value=0
    )
