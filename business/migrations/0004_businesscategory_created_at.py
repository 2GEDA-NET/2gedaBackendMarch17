# Generated by Django 4.2.5 on 2024-02-22 21:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_businessaccount_businessaddress_businesscategory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='businesscategory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
