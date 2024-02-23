# Generated by Django 4.2.5 on 2024-02-23 11:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0028_alter_ticket_ticket_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_key',
            field=models.UUIDField(default=uuid.UUID('1351fced-74cc-40c8-9910-8846930919bc')),
        ),
        migrations.AlterField(
            model_name='ticket_issues',
            name='error_key',
            field=models.UUIDField(default=uuid.UUID('9f9701a3-8ffe-4c52-a28a-98a45690079a')),
        ),
        migrations.AlterField(
            model_name='ticket_payment',
            name='payment_id',
            field=models.UUIDField(default=uuid.UUID('7ad82fd7-365e-4dce-b9fc-96cd7910cc4c')),
        ),
    ]
