# Generated by Django 5.0.6 on 2024-07-26 17:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_membre_solde'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membre',
            name='pack',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.pack'),
        ),
    ]