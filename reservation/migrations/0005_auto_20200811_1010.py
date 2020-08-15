# Generated by Django 3.1 on 2020-08-11 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0004_hotel_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='continent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservation.continent'),
        ),
        migrations.AddField(
            model_name='region',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservation.country'),
        ),
    ]