from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import secrets

class Profile(models.Model):   
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    email = models.EmailField(max_length=254, default = "")


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


def file_size(value):
    limit = 100 * 1024 * 1024
    print("Value Size: ", value.size)
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 100 MB.')

def user_directory_path(instance, filename):
    return 'videos/' + secrets.token_urlsafe(len(filename)) + '.mp4'

class Video(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    VideoPath = models.FileField(upload_to=user_directory_path, validators=[file_size], null=True, verbose_name="",)
    Name = models.CharField(max_length=100)

    def __str__(self):
        return "Video: " + str(self.VideoPath)


class Split(models.Model):
    SplitPath = models.CharField(max_length=400)

    def __str__(self):
        return str(str(self.id) +":" +self.SplitPath)

class VideoSplit(models.Model):
    VideoID = models.ForeignKey(Video, on_delete=models.CASCADE)
    SplitID = models.ForeignKey(Split, on_delete=models.CASCADE)

    def __str__(self):
        return self.VideoID

    class Meta:
        unique_together = (('VideoID', 'SplitID'),)

class SplitTranscript(models.Model):
    SplitID =  models.OneToOneField(Split, on_delete=models.CASCADE, primary_key=True)
    TranscriptPath = models.CharField(max_length=400)

    def __str__(self):
        return self.TranscriptPath

class SplitSpeech(models.Model):
    SplitID = models.OneToOneField(Split, on_delete=models.CASCADE, primary_key=True)
    SpeechPath = models.CharField(max_length=400)

    def __str__(self):
        return self.SpeechPath

class SplitSummary(models.Model):
    SplitID =  models.OneToOneField(Split, on_delete=models.CASCADE, primary_key=True)
    Summary = models.CharField(max_length=400)

    def __str__(self):
        return self.Summary

class SplitTag(models.Model):
    SplitID =  models.ForeignKey(Split, on_delete=models.CASCADE)
    Tag = models.CharField(max_length=50)

    def __str__(self):
        return str(self.SplitID)
    
    class Meta:
        unique_together = (('SplitID', 'Tag'),)

