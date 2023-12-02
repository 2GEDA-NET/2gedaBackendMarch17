# Generated by Django 4.2.5 on 2023-11-30 12:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0071_alter_event_event_id_alter_ticket_ticket_key_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_id',
        ),
        migrations.AlterField(
            model_name='event',
            name='event_key',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_key',
            field=models.UUIDField(default=uuid.UUID('fca048b1-8d69-4e6a-9d59-963be772a52e')),
        ),
        migrations.AlterField(
            model_name='ticket_issues',
            name='error_key',
            field=models.UUIDField(default=uuid.UUID('349c7ab3-93db-44ed-afa1-904573ce6989')),
        ),
        migrations.AlterField(
            model_name='ticket_payment',
            name='payment_id',
            field=models.UUIDField(default=uuid.UUID('0b52e062-a1ed-4281-9d34-66aa4b994358')),
        ),
    ]