# Generated by Django 3.2.9 on 2022-02-08 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0013_auto_20220207_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='name',
            field=models.CharField(blank=True, max_length=14),
        ),
    ]
