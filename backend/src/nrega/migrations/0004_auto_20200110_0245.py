# Generated by Django 3.0.2 on 2020-01-10 02:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nrega', '0003_auto_20200106_2310'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='filepath',
            new_name='s3_filepath',
        ),
    ]
