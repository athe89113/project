# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_knowledge', '0007_auto_20181018_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarmrule',
            name='time_end',
            field=models.CharField(max_length=20, null=True, verbose_name='\u7ed3\u675f\u65f6\u95f4', blank=True),
        ),
        migrations.AddField(
            model_name='alarmrule',
            name='time_start',
            field=models.CharField(max_length=20, null=True, verbose_name='\u5f00\u59cb\u65f6\u95f4', blank=True),
        ),
        migrations.AlterField(
            model_name='alarmrule',
            name='time_type',
            field=models.IntegerField(default=0, verbose_name='\u65f6\u95f4\u95f4\u9694\u7c7b\u578b'),
        ),
    ]
