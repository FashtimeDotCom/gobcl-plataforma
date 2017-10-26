# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 13:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ministries', '0002_auto_20171024_1030'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ministry',
            options={'ordering': ('importance',), 'verbose_name': 'ministry', 'verbose_name_plural': 'ministries'},
        ),
        migrations.AddField(
            model_name='ministry',
            name='importance',
            field=models.PositiveIntegerField(default=0, verbose_name='importance'),
        ),
        migrations.AlterField(
            model_name='ministry',
            name='public_servants',
            field=models.ManyToManyField(blank=True, related_name='ministries', to='public_servants.PublicServant', verbose_name='public servants'),
        ),
    ]
