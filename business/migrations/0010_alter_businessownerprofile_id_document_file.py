# Generated by Django 4.2.5 on 2024-02-23 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0009_remove_businessaccount_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessownerprofile',
            name='id_document_file',
            field=models.FileField(blank=True, null=True, upload_to='business-owner-docs', verbose_name='Identification Document Type'),
        ),
    ]
