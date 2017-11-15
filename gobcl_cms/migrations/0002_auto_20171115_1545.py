# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 18:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('gobcl_cms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HtmlPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='gobcl_cms_htmlplugin', serialize=False, to='cms.CMSPlugin')),
                ('html', models.TextField(verbose_name='html')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AlterField(
            model_name='imageplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='gobcl_cms_imageplugin', serialize=False, to='cms.CMSPlugin'),
        ),
    ]
