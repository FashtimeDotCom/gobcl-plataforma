# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 18:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ministries', '0009_auto_20171115_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='ministry',
            name='facebook',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ministry',
            name='twitter',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
