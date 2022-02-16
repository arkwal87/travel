# Generated by Django 3.2.9 on 2022-02-07 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0006_rename_contractproduct_contractother'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contracttrain',
            old_name='cabin_category',
            new_name='cabin_name',
        ),
        migrations.AddField(
            model_name='contractinsurance',
            name='insurance_no',
            field=models.CharField(default=2222, max_length=256),
            preserve_default=False,
        ),
    ]
