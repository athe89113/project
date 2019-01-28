# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_ssa', '0016_auto_20180802_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='ssareportresult',
            name='template_type',
            field=models.IntegerField(default=1),
        ),
    ]
