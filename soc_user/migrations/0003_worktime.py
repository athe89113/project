# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_user', '0002_auto_20180619_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('morning_start_time', models.DateTimeField(null=True, blank=True)),
                ('morning_end_time', models.DateTimeField(null=True, blank=True)),
                ('afternoon_start_time', models.DateTimeField(null=True, blank=True)),
                ('afternoon_end_time', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'work_time',
            },
        ),
    ]
