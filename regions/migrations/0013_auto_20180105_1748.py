# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-05 20:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0012_auto_20171206_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commune',
            name='twitter',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
