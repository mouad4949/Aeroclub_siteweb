# Generated by Django 5.0.6 on 2024-07-05 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_avions_description_avions_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='avions',
            name='nom',
            field=models.CharField(max_length=15, null=True),
        ),
    ]