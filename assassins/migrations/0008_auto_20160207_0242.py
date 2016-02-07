# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import encrypted_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('assassins', '0007_auto_20160207_0156'),
    ]

    operations = [
        migrations.CreateModel(
            name='DestroyLifeTokenKillAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_legal_target', models.BooleanField(help_text=b'Whether the victim was a legal target for the killer')),
                ('game_condition', models.CharField(default=b'', help_text=b'Game condition', max_length=1, blank=True, choices=[(b'', b'None'), (b'P', b'All other players eliminated'), (b'F', b'All other factions eliminated')])),
                ('role', models.CharField(max_length=1, choices=[(b'K', b'Killer'), (b'V', b'Victim')])),
                ('respawn_hours', models.PositiveSmallIntegerField(default=0, help_text=b'The player respawns in N hours (0 => no respawn)')),
                ('respawn_expiry_hours', models.PositiveIntegerField(default=0, help_text=b'Respawn life token expires N hours after becoming active')),
                ('killer_faction', models.ForeignKey(related_name='destroylifetokenkillaction_as_killer', to='assassins.Faction')),
                ('rules', models.ForeignKey(to='assassins.GameRules')),
                ('victim_faction', models.ForeignKey(related_name='destroylifetokenkillaction_as_victim', to='assassins.Faction')),
            ],
            options={
                'verbose_name': 'Destroy life token',
                'verbose_name_plural': 'Destroy life token actions',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='faction',
            name='min_starting_players',
            field=models.PositiveSmallIntegerField(default=0, help_text=b'Minimum number of players loyal to this faction at the start of the game'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='life_token',
            field=encrypted_fields.fields.EncryptedCharField(default=b'', help_text=b'Token indicating the player is alive', max_length=25, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='life_token_end_time',
            field=models.DateTimeField(default=None, help_text=b'When the life token expires (blank => until end of game)', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='life_token_start_time',
            field=models.DateTimeField(default=None, help_text=b'When the life token becomes usable (blank => usable immediately)', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='end_time',
            field=models.DateTimeField(default=None, help_text=b'When the game ends', null=True, blank=True),
            preserve_default=True,
        ),
    ]
