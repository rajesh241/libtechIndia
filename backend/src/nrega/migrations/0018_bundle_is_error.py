# Generated by Django 3.1 on 2020-11-25 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nrega', '0017_auto_20201125_0628'),
    ]

    operations = [
        migrations.AddField(
            model_name='bundle',
            name='is_error',
            field=models.BooleanField(default=False),
        ),
    ]