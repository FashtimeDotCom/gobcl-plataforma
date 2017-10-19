# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-19 13:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('government_structures', '0001_initial'),
        ('public_servants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commune',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='edition date', null=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('email', models.EmailField(max_length=100, verbose_name='email')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, verbose_name='phone')),
                ('twitter', models.CharField(max_length=50)),
                ('url', models.URLField(verbose_name='url')),
            ],
            options={
                'verbose_name': 'commune',
                'verbose_name_plural': 'communes',
                'permissions': (('view_commune', 'Can view communes'),),
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='edition date', null=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('email', models.EmailField(max_length=100, verbose_name='email')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, verbose_name='phone')),
                ('twitter', models.CharField(max_length=50)),
                ('url', models.URLField(verbose_name='url')),
                ('government_structure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='government_structures.GovernmentStructure', verbose_name='government structure')),
                ('governor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public_servants.PublicServant', verbose_name='governor')),
            ],
            options={
                'verbose_name': 'region',
                'verbose_name_plural': 'regions',
                'permissions': (('view_region', 'Can view regions'),),
            },
        ),
        migrations.AddField(
            model_name='commune',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='regions.Region', verbose_name='region'),
        ),
    ]
