# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('disk', '0002_auto_20150801_2307'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='headImg',
            new_name='File',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='username',
            new_name='uid',
        ),
    ]
