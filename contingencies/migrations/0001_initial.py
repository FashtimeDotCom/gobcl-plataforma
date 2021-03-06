# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-19 20:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contingency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='edition date', null=True)),
                ('is_active', models.BooleanField(default=False, verbose_name='is active')),
            ],
            options={
                'permissions': (('view_contingency', 'Can view contingency'),),
                'verbose_name': 'contingency',
                'verbose_name_plural': 'contingencies',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ContingencyEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='edition date', null=True)),
                ('url', models.URLField(blank=True, null=True, verbose_name='url')),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date time')),
                ('contingency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='contingencies.Contingency', verbose_name='contingency')),
            ],
            options={
                'ordering': ('-date_time',),
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ContingencyEventTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='contingencies.ContingencyEvent')),
            ],
            options={
                'db_tablespace': '',
                'default_permissions': (),
                'db_table': 'contingencies_contingencyevent_translation',
                'verbose_name': 'contingency event Translation',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ContingencyTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('lead', models.TextField(blank=True, verbose_name='lead')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='contingencies.Contingency')),
            ],
            options={
                'db_tablespace': '',
                'default_permissions': (),
                'db_table': 'contingencies_contingency_translation',
                'verbose_name': 'contingency Translation',
                'managed': True,
            },
        ),
        migrations.AlterUniqueTogether(
            name='contingencytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='contingencyeventtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
