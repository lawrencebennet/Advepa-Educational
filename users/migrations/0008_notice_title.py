# Generated by Django 4.1 on 2023-10-26 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_notice_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='title',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
