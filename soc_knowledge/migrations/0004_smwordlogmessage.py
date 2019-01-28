# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_knowledge', '0003_smword'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmWordLogMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=64)),
                ('word', models.CharField(max_length=100, null=True, verbose_name='\u540d\u79f0', blank=True)),
                ('sm_content', models.CharField(max_length=100, null=True, verbose_name='\u540d\u79f0', blank=True)),
                ('add_date', models.DateTimeField(null=True, blank=True)),
                ('level', models.IntegerField()),
            ],
            options={
                'db_table': 'sm_word_log_message',
            },
        ),
    ]
