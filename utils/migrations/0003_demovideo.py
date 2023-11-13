# Generated by Django 4.2.5 on 2023-11-11 12:28

from django.db import migrations, models
import utils.Customstorage


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0002_alter_demosong_audio_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Demovideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('cover_image', models.ImageField(default='default-audio.png', upload_to='cover-images/')),
                ('video_file', models.FileField(storage=utils.Customstorage.CustomS3Boto3Storage(), upload_to='video/', verbose_name='')),
            ],
        ),
    ]