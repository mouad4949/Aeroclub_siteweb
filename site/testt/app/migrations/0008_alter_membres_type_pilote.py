# Generated by Django 5.0.6 on 2024-07-03 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_membres_statut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membres',
            name='Type_pilote',
            field=models.CharField(choices=[('stagiaire', 'Stagiaire'), ('licence', 'Licence')], max_length=20, null=True),
        ),
    ]
