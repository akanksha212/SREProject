# Generated by Django 3.0.5 on 2020-04-23 07:52

from django.db import migrations, models
import summarize.models


class Migration(migrations.Migration):

    dependencies = [
        ('summarize', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='VideoPath',
            field=models.FileField(null=True, upload_to='videos/', validators=[summarize.models.file_size], verbose_name=''),
        ),
    ]
