# Generated by Django 4.2.5 on 2023-11-20 12:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0011_comment_responses_postmedia_comment_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmedia',
            name='is_business_post',
            field=models.BooleanField(default=False, verbose_name='Business Post'),
        ),
        migrations.AddField(
            model_name='postmedia',
            name='is_personal_post',
            field=models.BooleanField(default=True, verbose_name='Personal Post'),
        ),
        migrations.AddField(
            model_name='postmedia',
            name='tagged_users_post',
            field=models.ManyToManyField(blank=True, related_name='users_tag', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='HashTagsPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_tags', models.CharField(blank=True, max_length=256, null=True)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='feed.post')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='postmedia',
            name='hashtags',
            field=models.ManyToManyField(to='feed.hashtagspost'),
        ),
    ]