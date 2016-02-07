# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assassins', '0010_faction_max_staring_players'),
    ]

    operations = [
        migrations.RenameField(
            model_name='faction',
            old_name='max_staring_players',
            new_name='max_starting_players',
        ),
    ]
