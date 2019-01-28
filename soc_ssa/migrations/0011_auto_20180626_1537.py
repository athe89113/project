# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_ssa', '0010_auto_20180626_1510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seceventtype',
            name='type_match',
        ),
        migrations.RemoveField(
            model_name='seceventtype',
            name='type_value',
        ),
        migrations.AddField(
            model_name='seceventtype',
            name='type_items',
            field=models.TextField(default=b'[]'),
        ),
    ]
