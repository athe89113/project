# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_ssa', '0003_secdatatag_secfieldmap'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecEventType',
            fields=[
                ('tag', models.IntegerField(serialize=False, auto_created=True, primary_key=True)),
                ('type_name', models.CharField(max_length=100)),
                ('type_field', models.CharField(max_length=100, null=True, blank=True)),
                ('last_tag', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'sec_event_type',
                'verbose_name': '\u4e8b\u4ef6\u7c7b\u578b\u5bf9\u7167\u8868',
            },
        ),
    ]
