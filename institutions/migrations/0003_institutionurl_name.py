# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 13:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0002_auto_20171023_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutionurl',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
    ]
