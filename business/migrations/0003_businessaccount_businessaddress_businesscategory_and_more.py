# Generated by Django 4.2.5 on 2024-02-22 15:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_remove_userprofile_work_userprofile_occupation'),
        ('business', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=250, verbose_name='Business Name')),
                ('role', models.CharField(blank=True, max_length=250, null=True, verbose_name='Role')),
                ('image', models.ImageField(blank=True, null=True, upload_to='business-image/', verbose_name='Business Image')),
                ('about', models.TextField(blank=True, null=True, verbose_name='About')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Business Email')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Website')),
                ('is_verified', models.BooleanField(default=False, verbose_name='Verified')),
                ('founded_on', models.DateField(blank=True, null=True, verbose_name='Founded On')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(blank=True, default='Nigeria', max_length=20, null=True, verbose_name='Country')),
                ('state', models.CharField(blank=True, max_length=50, null=True, verbose_name='State')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='City')),
                ('street_address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Street Address')),
                ('zip_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='Zip Code')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.businessaccount', verbose_name='Business')),
            ],
            options={
                'verbose_name': 'Business Address',
                'verbose_name_plural': 'Business Addresses',
            },
        ),
        migrations.CreateModel(
            name='BusinessCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Category Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
            ],
        ),
        migrations.RemoveField(
            model_name='businessdirectory',
            name='address',
        ),
        migrations.RemoveField(
            model_name='businessdirectory',
            name='claimed_by',
        ),
        migrations.RemoveField(
            model_name='businessdirectory',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='businessownerprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='businessownerprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='businessownerprofile',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='businessownerprofile',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='businessownerprofile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='phonenumber',
            name='phone_number1',
        ),
        migrations.RemoveField(
            model_name='phonenumber',
            name='phone_number2',
        ),
        migrations.RemoveField(
            model_name='phonenumber',
            name='phone_number3',
        ),
        migrations.RemoveField(
            model_name='phonenumber',
            name='phone_number4',
        ),
        migrations.AddField(
            model_name='businessdocument',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.userprofile', verbose_name='User Profile'),
        ),
        migrations.AddField(
            model_name='businessdocument',
            name='tax_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Tax ID'),
        ),
        migrations.AddField(
            model_name='businessdocument',
            name='uploaded_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='businessownerprofile',
            name='id_document_file',
            field=models.FileField(blank=True, max_length=50, null=True, upload_to='business-owner-docs', verbose_name='Identification Document Type'),
        ),
        migrations.AddField(
            model_name='businessownerprofile',
            name='id_document_type',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Identification Document Type'),
        ),
        migrations.AddField(
            model_name='businessownerprofile',
            name='is_verified',
            field=models.BooleanField(default=False, verbose_name='Verified'),
        ),
        migrations.AddField(
            model_name='businessownerprofile',
            name='profile',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.userprofile', verbose_name='User Profile'),
        ),
        migrations.AddField(
            model_name='businessownerprofile',
            name='verified_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='phonenumber',
            name='phone1',
            field=models.CharField(default=2012121212, max_length=20, verbose_name='Phone 1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='phonenumber',
            name='phone2',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone 2'),
        ),
        migrations.AddField(
            model_name='phonenumber',
            name='phone3',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone 3'),
        ),
        migrations.AddField(
            model_name='phonenumber',
            name='phone4',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone 4'),
        ),
        migrations.AlterField(
            model_name='businessdocument',
            name='document_file',
            field=models.FileField(blank=True, null=True, upload_to='business-files/', verbose_name='Document File'),
        ),
        migrations.AlterField(
            model_name='businessdocument',
            name='document_type',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Document Type'),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.AddField(
            model_name='businessaccount',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.businesscategory', verbose_name='Business Category'),
        ),
        migrations.AddField(
            model_name='businessaccount',
            name='phone_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.phonenumber', verbose_name='Phone Number'),
        ),
        migrations.AddField(
            model_name='businessaccount',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userprofile', verbose_name='User Profile'),
        ),
        migrations.AlterField(
            model_name='businessdocument',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.businessaccount', verbose_name='Business'),
        ),
        migrations.DeleteModel(
            name='BusinessDirectory',
        ),
    ]
