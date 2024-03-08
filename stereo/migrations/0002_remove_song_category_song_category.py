# Generated by Django 4.2 on 2024-03-07 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stereo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='category',
        ),
        migrations.AddField(
            model_name='song',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stereo.songcategory', verbose_name='Category'),
        ),
    ]
