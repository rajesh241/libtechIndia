# Generated by Django 2.2.3 on 2019-07-28 05:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nrega', '0004_report'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='modified',
            new_name='updated',
        ),
    ]
