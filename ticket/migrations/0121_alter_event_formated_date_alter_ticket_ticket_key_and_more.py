# Generated by Django 4.2.5 on 2023-12-31 16:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0120_alter_event_formated_date_alter_ticket_ticket_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='formated_date',
            field=models.CharField(default='31 Dec, 2023'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_key',
            field=models.UUIDField(default=uuid.UUID('abf87470-c237-44e4-9d99-2c4b3dfce3be')),
        ),
        migrations.AlterField(
            model_name='ticket_issues',
            name='error_key',
            field=models.UUIDField(default=uuid.UUID('7f023145-f60d-4201-ade2-50de84e5cd49')),
        ),
        migrations.AlterField(
            model_name='ticket_payment',
            name='payment_id',
            field=models.UUIDField(default=uuid.UUID('e840769f-8497-43d4-949d-5035dc317be8')),
        ),
    ]
