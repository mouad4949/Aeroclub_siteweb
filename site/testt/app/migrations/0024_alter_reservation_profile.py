# Generated by Django 5.0.6 on 2024-07-12 21:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_alter_reservation_type_reservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile'),
        ),
    ]
