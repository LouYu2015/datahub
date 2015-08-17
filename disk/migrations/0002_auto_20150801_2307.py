# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('disk', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='file',
            new_name='User',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='head',
            new_name='headImg',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='uid',
            new_name='username',
        ),
    ]
