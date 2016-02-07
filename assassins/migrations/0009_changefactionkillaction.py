# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assassins', '0008_auto_20160207_0242'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeFactionKillAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_legal_target', models.BooleanField(help_text=b'Whether the victim was a legal target for the killer')),
                ('game_condition', models.CharField(default=b'', help_text=b'Game condition', max_length=1, blank=True, choices=[(b'', b'None'), (b'P', b'All other players eliminated'), (b'F', b'All other factions eliminated')])),
                ('role', models.CharField(max_length=1, choices=[(b'K', b'Killer'), (b'V', b'Victim')])),
                ('faction', models.ForeignKey(to='assassins.Faction')),
                ('killer_faction', models.ForeignKey(related_name='changefactionkillaction_as_killer', to='assassins.Faction')),
                ('rules', models.ForeignKey(to='assassins.GameRules')),
                ('victim_faction', models.ForeignKey(related_name='changefactionkillaction_as_victim', to='assassins.Faction')),
            ],
            options={
                'verbose_name': 'Change faction',
                'verbose_name_plural': 'Change faction actions',
            },
            bases=(models.Model,),
        ),
    ]
