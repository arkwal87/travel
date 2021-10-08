# Generated by Django 3.2.6 on 2021-09-29 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_contract', models.DateField()),
                ('client', models.ManyToManyField(to='reservation.Client')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contract_owner', to='reservation.client')),
            ],
        ),
        migrations.CreateModel(
            name='ContractRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
                ('contract', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservation.contract')),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservation.room')),
            ],
        ),
    ]
