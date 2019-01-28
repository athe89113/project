# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_ssa', '0014_ssaeventtype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ssaeventtype',
            old_name='event_one_types',
            new_name='event_one_type',
        ),
    ]
