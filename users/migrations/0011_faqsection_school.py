# Generated by Django 4.1 on 2023-11-04 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_faqsection_remove_faq_area_id_remove_faq_url_avatar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='faqsection',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.school'),
            preserve_default=False,
        ),
    ]
