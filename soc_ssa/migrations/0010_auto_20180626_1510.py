# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_ssa', '0009_auto_20180626_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='seceventtype',
            name='type_match',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='seceventtype',
            name='type_value',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
