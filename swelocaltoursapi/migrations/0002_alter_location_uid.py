# Generated by Django 4.1.3 on 2025-02-12 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swelocaltoursapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='uid',
            field=models.CharField(max_length=50),
        ),
    ]
