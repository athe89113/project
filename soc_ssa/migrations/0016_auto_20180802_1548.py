# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_ssa', '0015_auto_20180802_1543'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ssaeventtype',
            old_name='data_tag',
            new_name='data_tag_id',
        ),
    ]
