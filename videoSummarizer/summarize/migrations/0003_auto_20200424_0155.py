# Generated by Django 3.0.5 on 2020-04-23 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summarize', '0002_auto_20200423_1322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='split',
            name='EndTime',
        ),
        migrations.RemoveField(
            model_name='split',
            name='StartTime',
        ),
        migrations.AddField(
            model_name='split',
            name='SplitPath',
            field=models.CharField(default='', max_length=120),
            preserve_default=False,
        ),
    ]
