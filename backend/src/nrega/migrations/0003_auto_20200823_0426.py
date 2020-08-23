# Generated by Django 3.1 on 2020-08-22 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nrega', '0002_auto_20200823_0409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='display_name',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='libtech_tag',
            field=models.ManyToManyField(blank=True, to='nrega.LibtechTag'),
        ),
    ]
