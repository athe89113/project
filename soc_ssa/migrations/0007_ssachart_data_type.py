# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_ssa', '0006_ssareporttemplate_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='ssachart',
            name='data_type',
            field=models.IntegerField(default=0),
        ),
    ]
