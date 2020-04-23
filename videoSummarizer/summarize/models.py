from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

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


class Video(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    VideoPath = models.FileField(upload_to='videos/', validators=[file_size], null=True, verbose_name="",)

    def __str__(self):
        return "Video: " + str(self.VideoPath)


class Split(models.Model):
    StartTime = models.IntegerField()
    EndTime = models.IntegerField()

class VideoSplit(models.Model):
    VideoID = models.ForeignKey(Video, on_delete=models.CASCADE, primary_key=True)
    SplitID = models.ForeignKey(Split, on_delete=models.CASCADE)

class SplitTranscript(models.Model):
    SplitID =  models.ForeignKey(Split, on_delete=models.CASCADE, primary_key=True)
    TranscriptPath = models.CharField(max_length=120)

class SplitSpeech(models.Model):
    SplitID = models.ForeignKey(Split, on_delete=models.CASCADE, primary_key=True)
    SpeechPath = models.CharField(max_length=120)

class SplitSummary(models.Model):
    SplitID =  models.ForeignKey(Split, on_delete=models.CASCADE, primary_key=True)
    SummaryPath = models.CharField(max_length=120)

class SplitTag(models.Model):
    class Meta:
        unique_together = (('SplitID', 'Tag'),)

    SplitID =  models.ForeignKey(Split, on_delete=models.CASCADE)
    Tag = models.CharField(max_length=50)
