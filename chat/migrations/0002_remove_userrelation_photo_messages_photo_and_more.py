# Generated by Django 5.1.3 on 2025-04-16 20:01

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userrelation',
            name='Photo',
        ),
        migrations.AddField(
            model_name='messages',
            name='photo',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='images'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
