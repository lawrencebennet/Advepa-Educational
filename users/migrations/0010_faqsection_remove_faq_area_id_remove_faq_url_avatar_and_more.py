# Generated by Django 4.1 on 2023-11-04 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_faq_last_modify_alter_faq_area_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaqSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_id', models.CharField(choices=[('1', 'Sezione 1'), ('2', 'Sezione 2'), ('3', 'Sezione 3')], max_length=100)),
                ('url_avatar', models.CharField(default='https://models.readyplayer.me/63403f333dd6383c5cb59254.glb', max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='faq',
            name='area_id',
        ),
        migrations.RemoveField(
            model_name='faq',
            name='url_avatar',
        ),
        migrations.AddField(
            model_name='faq',
            name='section',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.faqsection'),
            preserve_default=False,
        ),
    ]
