# Generated by Django 4.2.5 on 2023-11-22 19:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticket', '0010_ticket_payment_payment_id_alter_ticket_ticket_key_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='withdraw',
            options={'get_latest_by': 'time_stamp'},
        ),
        migrations.AddField(
            model_name='withdraw',
            name='time_stamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='withdraw',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_key',
            field=models.UUIDField(default=uuid.UUID('e007fdb8-77e7-46ea-880e-b1f36bb25083')),
        ),
        migrations.AlterField(
            model_name='ticket_issues',
            name='error_key',
            field=models.UUIDField(default=uuid.UUID('0b7aca86-474a-4318-abc7-27f3e77e5173')),
        ),
        migrations.AlterField(
            model_name='ticket_payment',
            name='payment_id',
            field=models.UUIDField(default=uuid.UUID('7a6a700e-5faa-4372-bb47-5b8068cf0b07')),
        ),
    ]