# Generated by Django 5.0.6 on 2024-07-03 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_membres'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membres',
            name='Statut',
            field=models.CharField(default='Client', max_length=20),
        ),
    ]