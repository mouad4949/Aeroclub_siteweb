# Generated by Django 5.0.6 on 2024-07-20 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_reservation_date_de_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='duree',
            field=models.IntegerField(choices=[(5, '5 minutes'), (10, '10 minutes'), (15, '15 minutes'), (20, '20 minutes'), (25, '25 minutes'), (30, '30 minutes'), (35, '35 minutes'), (40, '40 minutes'), (45, '45 minutes'), (50, '50 minutes'), (55, '55 minutes'), (60, '60 minutes')], null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='Status',
            field=models.CharField(choices=[('en_attente', 'En Attente'), ('valide', 'Validé')], default='en attente', max_length=80),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='type_reservation',
            field=models.CharField(choices=[('vol_d_initiation', 'Vol d Initiation'), ('vol_decouverte', 'Vol Découverte')], max_length=80),
        ),
    ]
