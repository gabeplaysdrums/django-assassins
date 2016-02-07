# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assassins', '0005_auto_20160207_0136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='end_time',
            field=models.DateTimeField(help_text=b'When the game ends', null=True, blank=True),
            preserve_default=True,
        ),
    ]
