# Generated by Django 3.2.9 on 2022-01-30 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0005_auto_20220115_1241'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ContractProduct',
            new_name='ContractOther',
        ),
    ]
