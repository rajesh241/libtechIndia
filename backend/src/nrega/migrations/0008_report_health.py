# Generated by Django 3.1 on 2020-09-12 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nrega', '0007_taskqueue'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='health',
            field=models.CharField(blank=True, default='unknown', max_length=64, null=True),
        ),
    ]