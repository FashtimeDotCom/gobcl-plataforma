# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-05 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='iframe',
            field=models.TextField(blank=True, verbose_name='iframe'),
        ),
        migrations.AlterField(
            model_name='stream',
            name='url',
            field=models.URLField(blank=True, max_length=250, verbose_name='url'),
        ),
    ]
