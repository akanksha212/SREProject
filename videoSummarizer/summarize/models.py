# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.forms import ModelForm

class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=50)
    Password = models.CharField(max_length=25)

# Can merge Video and VideoUser table?
class Video(models.Model):
    VideoID = models.AutoField(primary_key=True)
    # VideoPath = models.CharField(max_length=120)
    VideoPath = models.FileField(upload_to='videos/', null=True, verbose_name="",)

    def __str__(self):
        return "Video: " + str(self.VideoPath)

class UserVideo(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    VideoID = models.ForeignKey(Video, on_delete=models.CASCADE,primary_key=True)

class Split(models.Model):
    SplitID =  models.AutoField(primary_key=True)
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
    SplitTagID = models.AutoField(primary_key=True)
    class Meta:
        unique_together = (('SplitID', 'Tag'),)

    SplitID =  models.ForeignKey(Split, on_delete=models.CASCADE)
    Tag = models.CharField(max_length=50)


# class VideoForm(ModelForm):
#     class Meta:
#         model= Video
#         fields= ["VideoID", "VideoPath"]

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
