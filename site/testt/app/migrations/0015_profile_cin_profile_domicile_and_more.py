# Generated by Django 5.0.6 on 2024-07-08 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_membership_date_abonnement_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='CIN',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Domicile',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='N_carte_stagiaire',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Nationalité',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Nom',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Ville',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='carte_validité',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='date_naissance',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='prenom',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='tel',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='etat_pilotage',
            field=models.CharField(blank=True, choices=[('pilote', 'Pilote'), ('non_pilote', 'Non_Pilote')], max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='type_pilote',
            field=models.CharField(blank=True, choices=[('pilote_licencié', 'Pilote_Licencié'), ('pilote_stagiaire', 'Pilote_Stagiaire')], max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='type_pilote_licencie',
            field=models.CharField(blank=True, choices=[('FI', 'Flight_Instructor'), ('GI', 'Ground_Instructor'), ('FE', 'Flight_Examinator')], max_length=80, null=True),
        ),
    ]