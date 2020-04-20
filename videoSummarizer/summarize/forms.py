from django import forms
from summarize.models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model= Video
        fields= ["VideoID", "VideoPath"]