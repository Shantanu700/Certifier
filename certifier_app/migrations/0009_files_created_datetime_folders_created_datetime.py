# Generated by Django 5.0 on 2025-01-10 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certifier_app', '0008_files_is_starred_folders_is_starred'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='created_datetime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='folders',
            name='created_datetime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
