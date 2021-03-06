# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-05 15:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public_enterprises', '0003_auto_20171205_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicEnterpriseTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=100, null=True, verbose_name='name')),
            ],
            options={
                'managed': True,
                'verbose_name': 'public enterprise Translation',
                'db_tablespace': '',
                'db_table': 'public_enterprises_publicenterprise_translation',
                'default_permissions': (),
            },
        ),
        migrations.RemoveField(
            model_name='publicenterprise',
            name='name',
        ),
        migrations.AddField(
            model_name='publicenterprisetranslation',
            name='master',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='public_enterprises.PublicEnterprise'),
        ),
        migrations.AlterUniqueTogether(
            name='publicenterprisetranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
