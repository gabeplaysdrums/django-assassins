# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assassins', '0006_auto_20160207_0140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='awardfixedpointskillaction',
            name='game_condition',
            field=models.CharField(default=b'', help_text=b'Game condition', max_length=1, blank=True, choices=[(b'', b'None'), (b'P', b'All other players eliminated'), (b'F', b'All other factions eliminated')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='declarehighestscoringplayerthewinnerkillaction',
            name='game_condition',
            field=models.CharField(default=b'', help_text=b'Game condition', max_length=1, blank=True, choices=[(b'', b'None'), (b'P', b'All other players eliminated'), (b'F', b'All other factions eliminated')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='declarekillersfactionthewinnerkillaction',
            name='game_condition',
            field=models.CharField(default=b'', help_text=b'Game condition', max_length=1, blank=True, choices=[(b'', b'None'), (b'P', b'All other players eliminated'), (b'F', b'All other factions eliminated')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='declarekillerthewinnerkillaction',
            name='game_condition',
            field=models.CharField(default=b'', help_text=b'Game condition', max_length=1, blank=True, choices=[(b'', b'None'), (b'P', b'All other players eliminated'), (b'F', b'All other factions eliminated')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='is_real_name_public',
            field=models.BooleanField(default=False, help_text=b"Whether the player's real name is public information"),
            preserve_default=True,
        ),
    ]
