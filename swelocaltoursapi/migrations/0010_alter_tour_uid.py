# Generated by Django 4.2.17 on 2025-02-05 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swelocaltoursapi', '0009_alter_tour_uid_alter_tour_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='uid',
            field=models.CharField(max_length=50),
        ),
    ]
