# Generated by Django 3.2.9 on 2022-02-28 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0020_auto_20220216_1735'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=100)),
                ('pdf', models.FileField(upload_to='media/pdfs')),
                ('contract', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservation.contract')),
            ],
        ),
        migrations.RemoveField(
            model_name='airport',
            name='country',
        ),
        migrations.DeleteModel(
            name='AirplaneRoutes',
        ),
        migrations.DeleteModel(
            name='Airport',
        ),
    ]
