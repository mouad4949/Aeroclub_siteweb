# Generated by Django 5.0.6 on 2024-07-08 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_alter_profile_type_pilote_licencie'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='titre',
            field=models.CharField(max_length=200, null=True),
        ),
    ]