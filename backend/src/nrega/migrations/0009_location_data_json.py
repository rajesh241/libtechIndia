# Generated by Django 3.0.7 on 2020-07-05 00:26

from django.db import migrations
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('nrega', '0008_auto_20200327_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='data_json',
            field=django_mysql.models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
