# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-16 19:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_enterprises', '0005_auto_20180312_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicenterprise',
            name='boost',
            field=models.FloatField(default=1.5, verbose_name='boost'),
        ),
    ]
