# Generated by Django 3.1 on 2020-08-22 11:11

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=256, unique=True)),
                ('otp_counter', models.PositiveIntegerField(default=0)),
                ('otp_expiration', models.DateTimeField(blank=True, null=True)),
                ('is_used', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'otp',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255, null=True, unique=True)),
                ('phone', models.CharField(max_length=255, null=True, unique=True)),
                ('user_role', models.CharField(blank=True, default='student', max_length=20, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('autogenerated_email', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('login_attempt_count', models.PositiveSmallIntegerField(default=0)),
                ('is_locked', models.BooleanField(default=False)),
                ('otp_counter', models.PositiveIntegerField(default=0)),
                ('otp_expiration', models.DateTimeField(blank=True, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=core.models.avatar_upload_path)),
                ('avatar_url', models.URLField(blank=True, max_length=1024, null=True)),
                ('provider', models.CharField(default='native', max_length=32)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
