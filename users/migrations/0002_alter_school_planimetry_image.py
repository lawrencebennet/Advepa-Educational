# Generated by Django 4.1 on 2023-10-23 16:39

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='planimetry_image',
            field=models.FileField(blank=True, null=True, upload_to=users.models.school_directory_path),
        ),
    ]
