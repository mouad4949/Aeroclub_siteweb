# Generated by Django 5.0.6 on 2024-07-17 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_reservation_nbrs_places_reservation_av_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='nbr_places',
            field=models.IntegerField(null=True),
        ),
    ]