# Generated by Django 5.2.2 on 2025-06-30 06:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_delete_bookingseat'),
        ('theaters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingSeat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.booking')),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theaters.seat')),
                ('show_time', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='theaters.showtime')),
            ],
        ),
    ]
