# Generated by Django 3.1 on 2020-08-17 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0018_auto_20200817_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomreservation',
            name='reservation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reservation.reservation'),
        ),
    ]