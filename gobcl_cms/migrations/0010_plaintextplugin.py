# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-21 13:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gobcl_cms', '0009_headerimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlainTextPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='gobcl_cms_plaintextplugin', serialize=False, to='cms.CMSPlugin')),
                ('text', models.TextField(verbose_name='text')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
