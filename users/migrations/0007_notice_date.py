# Generated by Django 4.1 on 2023-10-26 13:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_notice_media_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
