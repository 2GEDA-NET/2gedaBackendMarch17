# Generated by Django 4.2.5 on 2023-12-14 19:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0114_alter_ticket_ticket_key_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='is_free',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_key',
            field=models.UUIDField(default=uuid.UUID('a05ba0da-e743-46bf-a56c-27332553f7b2')),
        ),
        migrations.AlterField(
            model_name='ticket_issues',
            name='error_key',
            field=models.UUIDField(default=uuid.UUID('2675d362-d76b-49ad-8d59-c24239007e0e')),
        ),
        migrations.AlterField(
            model_name='ticket_payment',
            name='payment_id',
            field=models.UUIDField(default=uuid.UUID('c29f7a60-9abe-4d56-abe9-c27d1d9efe9f')),
        ),
    ]