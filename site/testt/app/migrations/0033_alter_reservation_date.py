# Generated by Django 5.0.6 on 2024-07-19 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_reservation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='date',
            field=models.DateTimeField(),
        ),
    ]