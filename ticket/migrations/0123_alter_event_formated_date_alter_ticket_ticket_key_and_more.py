# Generated by Django 4.2.5 on 2024-01-27 20:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0122_alter_event_formated_date_alter_ticket_ticket_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='formated_date',
            field=models.CharField(default='27 Jan, 2024'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_key',
            field=models.UUIDField(default=uuid.UUID('52589207-b219-4ba3-9fce-40860fa13dc2')),
        ),
        migrations.AlterField(
            model_name='ticket_issues',
            name='error_key',
            field=models.UUIDField(default=uuid.UUID('e867ed59-9adc-4c54-a8a1-f93b373350e7')),
        ),
        migrations.AlterField(
            model_name='ticket_payment',
            name='payment_id',
            field=models.UUIDField(default=uuid.UUID('7e8fdfb6-bf26-46f4-ae9c-7387b9a3a627')),
        ),
    ]
