# Generated by Django 5.0.6 on 2024-07-02 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='avions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('immatriculation', models.CharField(max_length=200, unique=True)),
                ('CDN', models.DateTimeField(verbose_name="date d'expiration ")),
                ('Licence_radio', models.DateTimeField(verbose_name='dete expi')),
                ('image', models.CharField(max_length=200)),
                ('Assurance', models.DateTimeField(verbose_name='date expir')),
                ('Nombres_de_places', models.IntegerField()),
            ],
        ),
    ]