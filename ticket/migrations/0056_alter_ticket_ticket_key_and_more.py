# Generated by Django 4.2.5 on 2023-11-28 10:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0055_alter_ticket_ticket_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_key',
            field=models.UUIDField(default=uuid.UUID('d75a2b03-7f91-4fe9-bbb8-f8a266759b0c')),
        ),
        migrations.AlterField(
            model_name='ticket_issues',
            name='error_key',
            field=models.UUIDField(default=uuid.UUID('3fa3fd14-4731-4fb0-aa06-14aa02fcf6f0')),
        ),
        migrations.AlterField(
            model_name='ticket_payment',
            name='payment_id',
            field=models.UUIDField(default=uuid.UUID('a888e83f-9aa2-4016-a8b7-70e830cf2fce')),
        ),
    ]