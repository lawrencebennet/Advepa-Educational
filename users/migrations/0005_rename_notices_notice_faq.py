# Generated by Django 4.1 on 2023-10-26 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_notices'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Notices',
            new_name='Notice',
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_id', models.CharField(choices=[('1', 'Section 1'), ('2', 'Section 2'), ('3', 'Section 3')], max_length=100)),
                ('url_avatar', models.CharField(default='https://models.readyplayer.me/63403f333dd6383c5cb59254.glb', max_length=100)),
                ('question', models.TextField(blank=True)),
                ('answer', models.TextField(blank=True)),
                ('link', models.CharField(blank=True, max_length=100)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.school')),
            ],
        ),
    ]
