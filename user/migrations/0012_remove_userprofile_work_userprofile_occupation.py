# Generated by Django 4.2.5 on 2024-02-21 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_userprofile_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='work',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='occupation',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Occupation'),
        ),
    ]
