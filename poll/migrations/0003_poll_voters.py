# Generated by Django 4.2.5 on 2024-03-07 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_blockedusers'),
        ('poll', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='voters',
            field=models.ManyToManyField(blank=True, related_name='poll_voters', to='user.userprofile', verbose_name='Voters'),
        ),
    ]
