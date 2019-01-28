# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_ssa', '0011_auto_20180626_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secfieldmap',
            name='field_priority',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
