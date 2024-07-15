from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'displayname', 'info', 'interests','gender',]
        widgets = {
            'image': forms.FileInput(),
            'displayname' : forms.TextInput(attrs={'placeholder': 'Add display name'}),
            'info' : forms.Textarea(attrs={'rows':3, 'placeholder': 'Add information'}),
            'phone' : forms.Textarea(attrs={'rows':3, 'placeholder': 'Add phone number'}),
            'interests' : forms.Select(choices=[('love','love'),('nostrings','nostrings'),('hookups','hookups'),('friendship','friendship')]),
            'gender' : forms.Select(choices=[('male','male'),('female','female'),('other','other')]),
        }
        
        
class EmailForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']
