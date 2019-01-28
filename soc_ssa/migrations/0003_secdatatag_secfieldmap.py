# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc', '0002_auto_20180619_1607'),
        ('soc_ssa', '0002_auto_20180619_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='SECDataTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('path', models.CharField(max_length=256)),
                ('time_format', models.CharField(default=b'yyyy-MM-dd-HH', max_length=256)),
                ('agent', models.ForeignKey(blank=True, to='soc.Agent', null=True)),
                ('company', models.ForeignKey(blank=True, to='soc.Company', null=True)),
            ],
            options={
                'db_table': 'sec_data_tag',
                'verbose_name': '\u6570\u636e\u6807\u7b7e',
            },
        ),
        migrations.CreateModel(
            name='SECFieldMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=256)),
                ('precedence', models.IntegerField(default=0)),
                ('items', models.TextField(default=b'[]')),
                ('data_tag', models.ForeignKey(blank=True, to='soc_ssa.SECDataTag', null=True)),
            ],
            options={
                'db_table': 'sec_field_map',
            },
        ),
    ]
