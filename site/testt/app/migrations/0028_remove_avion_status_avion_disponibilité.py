# Generated by Django 5.0.6 on 2024-07-15 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_membre_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='avion',
            name='status',
        ),
        migrations.AddField(
            model_name='avion',
            name='Disponibilité',
            field=models.BooleanField(default=1),
        ),
    ]
