# Generated by Django 5.0.6 on 2024-07-02 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_news_date_alter_news_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.CharField(max_length=200),
        ),
    ]
