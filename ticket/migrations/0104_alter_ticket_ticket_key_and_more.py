# Generated by Django 4.2.5 on 2023-12-09 14:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0103_alter_ticket_ticket_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_key',
            field=models.UUIDField(default=uuid.UUID('52a46e6c-f2e0-4526-8a7e-04fa57cb5634')),
        ),
        migrations.AlterField(
            model_name='ticket_issues',
            name='error_key',
            field=models.UUIDField(default=uuid.UUID('9dc0fa4f-b40b-4984-a4a5-ace14b3f7740')),
        ),
        migrations.AlterField(
            model_name='ticket_payment',
            name='payment_id',
            field=models.UUIDField(default=uuid.UUID('dc4b4c7d-8f2c-414f-8354-4ab8eafdba6e')),
        ),
    ]