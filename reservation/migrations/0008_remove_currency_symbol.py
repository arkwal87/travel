# Generated by Django 3.1 on 2020-08-11 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0007_auto_20200811_1319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currency',
            name='symbol',
        ),
    ]
