# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-05 15:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public_servants', '0006_auto_20171129_1649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicservant',
            name='charge_en',
        ),
        migrations.RemoveField(
            model_name='publicservant',
            name='charge_es',
        ),
        migrations.RemoveField(
            model_name='publicservant',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='publicservant',
            name='description_es',
        ),
    ]
