# Generated by Django 3.2.6 on 2021-11-03 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0007_auto_20211016_1206'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractVilla',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
                ('price_offer', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_net', models.DecimalField(decimal_places=2, max_digits=10)),
                ('contract', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservation.contract')),
                ('counterparty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.counterparty')),
                ('net_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='net_villa_currency', to='reservation.currency')),
                ('offer_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_villa_currency', to='reservation.currency')),
                ('villa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservation.villa')),
            ],
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='client',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='reservation2',
            name='counterparty',
        ),
        migrations.RemoveField(
            model_name='reservation2',
            name='hotel',
        ),
        migrations.RemoveField(
            model_name='reservation2',
            name='meal_plan',
        ),
        migrations.RemoveField(
            model_name='reservation2',
            name='net_currency',
        ),
        migrations.RemoveField(
            model_name='reservation2',
            name='offer_currency',
        ),
        migrations.RemoveField(
            model_name='reservation2',
            name='room_category',
        ),
        migrations.RemoveField(
            model_name='roomreservation',
            name='reservation',
        ),
        migrations.RemoveField(
            model_name='roomreservation',
            name='room',
        ),
        migrations.AlterField(
            model_name='contractroom',
            name='net_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='net_room_currency', to='reservation.currency'),
        ),
        migrations.AlterField(
            model_name='contractroom',
            name='offer_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_room_currency', to='reservation.currency'),
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='Reservation',
        ),
        migrations.DeleteModel(
            name='Reservation2',
        ),
        migrations.DeleteModel(
            name='RoomReservation',
        ),
    ]
