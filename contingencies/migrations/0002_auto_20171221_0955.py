# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-21 12:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('contingencies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContingencyInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='edition date', null=True)),
                ('url', models.URLField(null=True, verbose_name='url')),
                ('contingency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='informations', to='contingencies.Contingency', verbose_name='contingency')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ContingencyInformationTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='contingencies.ContingencyInformation')),
            ],
            options={
                'verbose_name': 'contingency information Translation',
                'db_table': 'contingencies_contingencyinformation_translation',
                'default_permissions': (),
                'managed': True,
                'db_tablespace': '',
            },
        ),
        migrations.AlterUniqueTogether(
            name='contingencyinformationtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
