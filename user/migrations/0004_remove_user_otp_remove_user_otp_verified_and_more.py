# Generated by Django 4.2.5 on 2024-02-17 07:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_managers_alter_user_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='otp',
        ),
        migrations.RemoveField(
            model_name='user',
            name='otp_verified',
        ),
        migrations.CreateModel(
            name='OneTimePassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=5, verbose_name='OTP')),
                ('verification_type', models.CharField(choices=[('account_verification', 'Email Verification'), ('password_verification', 'Password Verification')], max_length=25, verbose_name='Verification Type')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='one_time_password', to=settings.AUTH_USER_MODEL, verbose_name='Auth User')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
