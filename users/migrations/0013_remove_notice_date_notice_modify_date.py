# Generated by Django 4.1 on 2023-11-04 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_remove_faq_school'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice',
            name='date',
        ),
        migrations.AddField(
            model_name='notice',
            name='modify_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
