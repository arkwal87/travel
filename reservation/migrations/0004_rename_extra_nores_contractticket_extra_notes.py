# Generated by Django 3.2.9 on 2022-01-15 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_contractticket_extra_nores'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contractticket',
            old_name='extra_nores',
            new_name='extra_notes',
        ),
    ]