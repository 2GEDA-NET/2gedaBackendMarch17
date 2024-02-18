# Generated by Django 4.2.5 on 2024-02-07 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stereo', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chart',
            name='song',
        ),
        migrations.RemoveField(
            model_name='downloadrecord',
            name='song',
        ),
        migrations.RemoveField(
            model_name='downloadrecord',
            name='user',
        ),
        migrations.RemoveField(
            model_name='musicprofile',
            name='favorite_genre',
        ),
        migrations.RemoveField(
            model_name='musicprofile',
            name='listening_history',
        ),
        migrations.RemoveField(
            model_name='musicprofile',
            name='playlists',
        ),
        migrations.RemoveField(
            model_name='musicprofile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='playlist',
            name='songs',
        ),
        migrations.RemoveField(
            model_name='playlist',
            name='user',
        ),
        migrations.RemoveField(
            model_name='song',
            name='album',
        ),
        migrations.RemoveField(
            model_name='song',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='stereoaccount',
            name='profile',
        ),
        migrations.AlterUniqueTogether(
            name='usersongpreference',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='usersongpreference',
            name='song',
        ),
        migrations.RemoveField(
            model_name='usersongpreference',
            name='user',
        ),
        migrations.DeleteModel(
            name='Album',
        ),
        migrations.DeleteModel(
            name='Artist',
        ),
        migrations.DeleteModel(
            name='Chart',
        ),
        migrations.DeleteModel(
            name='DownloadRecord',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
        migrations.DeleteModel(
            name='MusicProfile',
        ),
        migrations.DeleteModel(
            name='Playlist',
        ),
        migrations.DeleteModel(
            name='Song',
        ),
        migrations.DeleteModel(
            name='StereoAccount',
        ),
        migrations.DeleteModel(
            name='UserSongPreference',
        ),
    ]