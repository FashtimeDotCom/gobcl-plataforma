# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-21 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ministries', '0013_auto_20171221_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ministry',
            name='facebook',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='ministry',
            name='twitter',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
