# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boh', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='users_records',
            new_name='user_records',
        ),
    ]
