# Generated by Django 4.2.5 on 2024-02-17 06:46

from django.db import migrations, models
import user.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_coverimagemedia_alter_userprofile_cover_image"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", user.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(default="me@you.com", max_length=254, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(default="012555555", max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
