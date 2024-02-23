# Generated by Django 4.2.5 on 2024-02-21 16:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0009_alter_ticket_ticket_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_key',
            field=models.UUIDField(default=uuid.UUID('d9230b5c-12c6-493f-8b7a-841f5d9edf75')),
        ),
        migrations.AlterField(
            model_name='ticket_issues',
            name='error_key',
            field=models.UUIDField(default=uuid.UUID('eb2b075a-453a-4367-85bb-07d62a5d8a52')),
        ),
        migrations.AlterField(
            model_name='ticket_payment',
            name='payment_id',
            field=models.UUIDField(default=uuid.UUID('34cfc3c9-54be-4cb1-ac2d-0000d1569de8')),
        ),
    ]
