# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 22:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0005_auto_20171027_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='commune',
            name='has_own_municipality',
            field=models.BooleanField(default=True),
        ),
    ]
