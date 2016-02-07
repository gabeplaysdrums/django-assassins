# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assassins', '0004_auto_20160207_0119'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gamerules',
            options={'verbose_name_plural': 'Game rules'},
        ),
        migrations.AddField(
            model_name='player',
            name='pseudonym',
            field=models.CharField(default='', help_text=b"Pseudonym used for this game in place of the user's real name", max_length=100),
            preserve_default=False,
        ),
    ]
