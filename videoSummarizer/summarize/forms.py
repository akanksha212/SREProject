from django import forms
from summarize.models import Video
from django.contrib.admin import widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import PasswordInput


class VideoForm(forms.ModelForm):
    class Meta:
        model= Video
        fields= ["VideoPath"]


def clean_unique(form, field, exclude_initial=True, 
                 format="The %(field)s %(value)s has already been taken."):
    value = form.cleaned_data.get(field)
    if value:
        qs = form._meta.model._default_manager.filter(**{field:value})
        if exclude_initial and form.initial:
            initial_value = form.initial.get(field)
            qs = qs.exclude(**{field:initial_value})
        if qs.count() > 0:
            raise forms.ValidationError(format % {'field':field, 'value':value})
    return value



class SignUpForm(UserCreationForm):

    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder' : 'Username'}))
    email = forms.EmailField(max_length=254,  widget=forms.TextInput(attrs={'placeholder' : 'Email'}))
    first_name = forms.CharField(max_length=254,  widget=forms.TextInput(attrs={'placeholder' : 'First Name'}))
    last_name = forms.CharField(max_length=254,  widget=forms.TextInput(attrs={'placeholder' : 'Last Name'}))
        
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',)

    def clean_username(self):
        return clean_unique(self, 'username')
    
    def clean_email(self):
        return clean_unique(self, 'email')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
