# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_ssa', '0007_ssachart_data_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ssachart',
            name='data_tag',
            field=models.IntegerField(default=0),
        ),
    ]
