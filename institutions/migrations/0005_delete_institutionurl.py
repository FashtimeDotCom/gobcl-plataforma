# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 14:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ministries', '0004_auto_20171025_1126'),
        ('institutions', '0004_auto_20171024_1037'),
    ]

    operations = [
        migrations.DeleteModel(
            name='InstitutionURL',
        ),
    ]
