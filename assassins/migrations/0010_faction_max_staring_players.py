# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assassins', '0009_changefactionkillaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='faction',
            name='max_staring_players',
            field=models.PositiveSmallIntegerField(default=0, help_text=b'Maximum number of players loyal to this faction at the start of the game (0 => no maximum)'),
            preserve_default=True,
        ),
    ]
