# Generated by Django 4.2.5 on 2023-11-27 21:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0029_alter_ticket_ticket_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_key',
            field=models.UUIDField(default=uuid.UUID('59080ef5-1420-4085-9fa1-454b26b66fab')),
        ),
        migrations.AlterField(
            model_name='ticket_issues',
            name='error_key',
            field=models.UUIDField(default=uuid.UUID('d8316055-2754-4070-a884-b3212dc6a9e6')),
        ),
        migrations.AlterField(
            model_name='ticket_payment',
            name='payment_id',
            field=models.UUIDField(default=uuid.UUID('3240a366-eafc-434e-8803-725bf4ddb929')),
        ),
    ]