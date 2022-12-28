# Generated by Django 4.1.4 on 2022-12-25 17:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_booking_reservation_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order_time',
        ),
        migrations.AddField(
            model_name='order',
            name='order_time',
            field=models.TimeField(default=datetime.datetime(2022, 12, 25, 20, 41, 36, 80974)),
        ),
        migrations.AlterField(
            model_name='room',
            name='booking',
            field=models.BooleanField(choices=[(True, 'Yoqish'), (False, "O'chirish")], default=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='is_booked',
            field=models.BooleanField(choices=[(True, 'Bron qilish'), (False, 'Brondan chiqarish')], default=False),
        ),
    ]