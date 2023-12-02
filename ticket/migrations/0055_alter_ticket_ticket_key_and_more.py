# Generated by Django 4.2.5 on 2023-11-28 10:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0054_alter_ticket_ticket_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_key',
            field=models.UUIDField(default=uuid.UUID('3ff75a5f-a75d-42d0-988a-966ed4efcebb')),
        ),
        migrations.AlterField(
            model_name='ticket_issues',
            name='error_key',
            field=models.UUIDField(default=uuid.UUID('4cd421b7-f583-4aab-8e67-7c4cb03b8ab2')),
        ),
        migrations.AlterField(
            model_name='ticket_payment',
            name='payment_id',
            field=models.UUIDField(default=uuid.UUID('97ae59a0-fb9f-488d-992c-bd014ed3cd84')),
        ),
    ]