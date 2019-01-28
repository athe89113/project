# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_knowledge', '0002_auto_20180619_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmWord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word', models.CharField(max_length=100, null=True, verbose_name='\u540d\u79f0', blank=True)),
            ],
            options={
                'db_table': 'sm_word',
            },
        ),
    ]
