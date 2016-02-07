# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('assassins', '0002_auto_20160206_2139'),
    ]

    operations = [
        migrations.CreateModel(
            name='AwardFixedPointsKillAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_legal_target', models.BooleanField(help_text=b'Whether the victim was a legal target for the killer')),
                ('game_condition', models.CharField(default=b'', help_text=b'Game condition', max_length=1, choices=[(b'', b'None'), (b'P', b'All other players eliminated'), (b'F', b'All other factions eliminated')])),
                ('role', models.CharField(max_length=1, choices=[(b'K', b'Killer'), (b'V', b'Victim')])),
                ('points', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeclareHighestScoringPlayerTheWinnerKillAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_legal_target', models.BooleanField(help_text=b'Whether the victim was a legal target for the killer')),
                ('game_condition', models.CharField(default=b'', help_text=b'Game condition', max_length=1, choices=[(b'', b'None'), (b'P', b'All other players eliminated'), (b'F', b'All other factions eliminated')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeclareKillersFactionTheWinnerKillAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_legal_target', models.BooleanField(help_text=b'Whether the victim was a legal target for the killer')),
                ('game_condition', models.CharField(default=b'', help_text=b'Game condition', max_length=1, choices=[(b'', b'None'), (b'P', b'All other players eliminated'), (b'F', b'All other factions eliminated')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeclareKillerTheWinnerKillAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_legal_target', models.BooleanField(help_text=b'Whether the victim was a legal target for the killer')),
                ('game_condition', models.CharField(default=b'', help_text=b'Game condition', max_length=1, choices=[(b'', b'None'), (b'P', b'All other players eliminated'), (b'F', b'All other factions eliminated')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Faction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Display name', max_length=100)),
                ('max_assigned_targets', models.PositiveSmallIntegerField(default=0, help_text=b'Maximum number of targets a player can be assigned from this faction')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Display name', max_length=100)),
                ('start_time', models.DateTimeField(help_text=b'When the game starts')),
                ('end_time', models.DateTimeField(help_text=b'When the game ends', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GameRules',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Display name', max_length=100)),
                ('max_assigned_targets', models.PositiveSmallIntegerField(default=0, help_text=b'Maximum number of assigned targets (0 => no assigned targets)')),
                ('assign_targets_in_own_faction', models.BooleanField(default=False, help_text=b'Whether a player can have assigned targets in their own faction')),
                ('expiry_days', models.PositiveSmallIntegerField(default=0, help_text=b'Number of days after start when the game automatically ends (0 => no time limit)')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GameWinner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('faction', models.ForeignKey(to='assassins.Faction', help_text=b'Faction who won the game', null=True)),
                ('game', models.OneToOneField(related_name='winner', to='assassins.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0, help_text=b'Current score (higher is better)')),
                ('is_real_name_public', models.BooleanField(default=False, help_text=b'Whether the players real name is public information')),
                ('is_legal_target_for_all_players', models.BooleanField(default=False, help_text=b'Whether the player is a legal target for all other players')),
                ('faction', models.ForeignKey(related_name='players', to='assassins.Faction')),
                ('game', models.ForeignKey(related_name='players', to='assassins.Game')),
                ('user', models.ForeignKey(related_name='players', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='gamewinner',
            name='player',
            field=models.ForeignKey(to='assassins.Player', help_text=b'Player who won the game', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='rules',
            field=models.ForeignKey(to='assassins.GameRules'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='faction',
            name='rules',
            field=models.ForeignKey(related_name='factions', to='assassins.GameRules'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='declarekillerthewinnerkillaction',
            name='killer_faction',
            field=models.ForeignKey(related_name='declarekillerthewinnerkillaction_as_killer', to='assassins.Faction'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='declarekillerthewinnerkillaction',
            name='rules',
            field=models.ForeignKey(to='assassins.GameRules'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='declarekillerthewinnerkillaction',
            name='victim_faction',
            field=models.ForeignKey(related_name='declarekillerthewinnerkillaction_as_victim', to='assassins.Faction'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='declarekillersfactionthewinnerkillaction',
            name='killer_faction',
            field=models.ForeignKey(related_name='declarekillersfactionthewinnerkillaction_as_killer', to='assassins.Faction'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='declarekillersfactionthewinnerkillaction',
            name='rules',
            field=models.ForeignKey(to='assassins.GameRules'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='declarekillersfactionthewinnerkillaction',
            name='victim_faction',
            field=models.ForeignKey(related_name='declarekillersfactionthewinnerkillaction_as_victim', to='assassins.Faction'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='declarehighestscoringplayerthewinnerkillaction',
            name='killer_faction',
            field=models.ForeignKey(related_name='declarehighestscoringplayerthewinnerkillaction_as_killer', to='assassins.Faction'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='declarehighestscoringplayerthewinnerkillaction',
            name='rules',
            field=models.ForeignKey(to='assassins.GameRules'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='declarehighestscoringplayerthewinnerkillaction',
            name='victim_faction',
            field=models.ForeignKey(related_name='declarehighestscoringplayerthewinnerkillaction_as_victim', to='assassins.Faction'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='awardfixedpointskillaction',
            name='killer_faction',
            field=models.ForeignKey(related_name='awardfixedpointskillaction_as_killer', to='assassins.Faction'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='awardfixedpointskillaction',
            name='rules',
            field=models.ForeignKey(to='assassins.GameRules'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='awardfixedpointskillaction',
            name='victim_faction',
            field=models.ForeignKey(related_name='awardfixedpointskillaction_as_victim', to='assassins.Faction'),
            preserve_default=True,
        ),
    ]
