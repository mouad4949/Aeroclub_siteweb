# Generated by Django 5.0.6 on 2024-07-26 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_pack_membre_pack'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pack',
            name='Minutes',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='pack',
            name='type',
            field=models.CharField(max_length=80),
        ),
    ]
