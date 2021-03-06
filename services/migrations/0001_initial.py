# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-20 12:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChileAtiendeFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='edition date', null=True)),
                ('service_name', models.CharField(max_length=255, verbose_name='service name')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('code', models.CharField(max_length=255, unique=True, verbose_name='code')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name='date')),
                ('objective', models.TextField(verbose_name='objective')),
                ('beneficiaries', models.TextField(verbose_name='beneficiaries')),
                ('cost', models.TextField(verbose_name='cost')),
                ('period', models.TextField(verbose_name='period')),
                ('duration', models.TextField(verbose_name='duration')),
                ('analytic_visits', models.PositiveIntegerField(default=0, verbose_name='analytic visits')),
            ],
            options={
                'ordering': ('-analytic_visits',),
            },
        ),
        migrations.CreateModel(
            name='ChileAtiendeService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='edition date', null=True)),
                ('code', models.CharField(max_length=255, unique=True, verbose_name='code')),
                ('initial', models.CharField(blank=True, max_length=255, null=True, verbose_name='initial')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('url', models.URLField(blank=True, null=True, verbose_name='url')),
                ('mision', models.TextField(verbose_name='mision')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='chileatiendefile',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files', to='services.ChileAtiendeService', verbose_name='service'),
        ),
    ]
