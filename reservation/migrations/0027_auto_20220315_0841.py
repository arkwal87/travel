# Generated by Django 3.2.9 on 2022-03-15 07:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0026_alter_client_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractroom',
            name='price_net',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='contractroom',
            name='price_offer',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]