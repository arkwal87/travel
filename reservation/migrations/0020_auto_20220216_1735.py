# Generated by Django 3.2.9 on 2022-02-16 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0019_rename_bankaccounts_bankaccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractticket',
            name='extra_notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contractticket',
            name='ticket_details',
            field=models.TextField(blank=True, null=True),
        ),
    ]