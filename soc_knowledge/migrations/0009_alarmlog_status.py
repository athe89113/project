# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_knowledge', '0008_auto_20181018_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarmlog',
            name='status',
            field=models.IntegerField(default=1, verbose_name='\u72b6\u6001'),
        ),
    ]
