# Generated by Django 5.0.6 on 2024-07-25 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_alter_biens_reservations_prix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biens_reservations',
            name='prix',
            field=models.IntegerField(null=True),
        ),
    ]
