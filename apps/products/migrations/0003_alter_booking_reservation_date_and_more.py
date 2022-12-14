# Generated by Django 4.1.4 on 2022-12-25 13:54

import apps.products.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_booking_reservation_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='reservation_date',
            field=models.DateTimeField(blank=True, null=True, validators=[apps.products.models.Booking.validate_date]),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order_time',
            field=models.TimeField(default=datetime.datetime(2022, 12, 25, 16, 54, 43, 663431)),
        ),
    ]
