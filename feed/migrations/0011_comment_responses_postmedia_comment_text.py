# Generated by Django 4.2.5 on 2023-11-20 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0010_alter_comment_media_mediapost_postmedia_each_media'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='responses',
            field=models.ManyToManyField(related_name='commnts_to_reply', to='feed.reply'),
        ),
        migrations.AddField(
            model_name='postmedia',
            name='comment_text',
            field=models.ManyToManyField(to='feed.comment'),
        ),
    ]