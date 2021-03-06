# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 21:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_servants', '0004_auto_20171030_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicservant',
            name='charge_en',
            field=models.CharField(max_length=100, null=True, verbose_name='charge'),
        ),
        migrations.AddField(
            model_name='publicservant',
            name='charge_es',
            field=models.CharField(max_length=100, null=True, verbose_name='charge'),
        ),
        migrations.AddField(
            model_name='publicservant',
            name='description_en',
            field=models.TextField(null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='publicservant',
            name='description_es',
            field=models.TextField(null=True, verbose_name='description'),
        ),
    ]
