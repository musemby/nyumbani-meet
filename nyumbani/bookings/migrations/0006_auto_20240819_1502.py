# Generated by Django 3.2.8 on 2024-08-19 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_auto_20240730_0553'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='operates_from',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='operates_to',
            field=models.TimeField(blank=True, null=True),
        ),
    ]