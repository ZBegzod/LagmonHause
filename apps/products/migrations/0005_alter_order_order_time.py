# Generated by Django 4.1.4 on 2022-12-25 18:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_remove_orderitem_order_time_order_order_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.TimeField(default=datetime.datetime(2022, 12, 25, 21, 31, 39, 867122)),
        ),
    ]