# Generated by Django 4.1.3 on 2025-02-12 00:42

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=255)),
                ('coordinates', models.JSONField(default=dict)),
                ('uid', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('bio', models.CharField(max_length=280)),
                ('uid', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=280)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('duration', models.IntegerField(default=60)),
                ('uid', models.CharField(max_length=50)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tours', to='swelocaltoursapi.location')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tours_created', to='swelocaltoursapi.user')),
            ],
        ),
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itineraries', to='swelocaltoursapi.tour')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itineraries', to='swelocaltoursapi.user')),
            ],
        ),
    ]
