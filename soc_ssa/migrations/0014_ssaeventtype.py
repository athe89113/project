# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_ssa', '0013_ssareporttemplate_template_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='SSAEventType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_tag', models.IntegerField()),
                ('event_two_type', models.CharField(max_length=500)),
                ('event_three_types', models.CharField(max_length=500, null=True, blank=True)),
                ('event_one_types', models.CharField(max_length=500, null=True, blank=True)),
            ],
            options={
                'db_table': 'ssa_event_type',
                'verbose_name': '\u4e8b\u4ef6\u7c7b\u578b\u5bf9\u7167\u8868',
            },
        ),
    ]
