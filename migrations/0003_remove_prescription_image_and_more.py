# Generated by Django 5.2.1 on 2025-06-06 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='image',
        ),
        migrations.AddField(
            model_name='prescription',
            name='prescription_file',
            field=models.FileField(blank=True, null=True, upload_to='prescriptions/'),
        ),
    ]
