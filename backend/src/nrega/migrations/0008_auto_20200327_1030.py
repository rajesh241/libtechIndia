# Generated by Django 3.0.2 on 2020-03-27 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nrega', '0007_taskqueue_location_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='accuracy',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='is_data_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='location',
            name='last_crawl_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
