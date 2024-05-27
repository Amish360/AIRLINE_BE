# Generated by Django 4.0.3 on 2024-05-25 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=255)),
                ('manufacturer', models.CharField(max_length=255)),
                ('capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_number', models.CharField(max_length=10)),
                ('scheduled_departure', models.DateTimeField()),
                ('scheduled_arrival', models.DateTimeField()),
                ('status', models.CharField(choices=[('Scheduled', 'Scheduled'), ('On Time', 'On Time'), ('Delayed', 'Delayed'), ('Cancelled', 'Cancelled'), ('Landed', 'Landed')], max_length=50)),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airline_app.aircraft')),
                ('airline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airline_app.airline')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrivals', to='airline_app.airport')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departures', to='airline_app.airport')),
            ],
        ),
        migrations.CreateModel(
            name='FlightStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_departure', models.DateTimeField(blank=True, null=True)),
                ('updated_arrival', models.DateTimeField(blank=True, null=True)),
                ('gate', models.CharField(blank=True, max_length=10, null=True)),
                ('remarks', models.CharField(blank=True, max_length=255, null=True)),
                ('flight', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='airline_app.flight')),
            ],
        ),
    ]
