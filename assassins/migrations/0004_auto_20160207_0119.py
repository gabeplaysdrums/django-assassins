# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assassins', '0003_auto_20160207_0114'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='awardfixedpointskillaction',
            options={'verbose_name': 'Award fixed points', 'verbose_name_plural': 'Award fixed points actions'},
        ),
        migrations.AlterModelOptions(
            name='declarehighestscoringplayerthewinnerkillaction',
            options={'verbose_name': 'Declare highest player the winnner', 'verbose_name_plural': 'Declare highest player the winner actions'},
        ),
        migrations.AlterModelOptions(
            name='declarekillersfactionthewinnerkillaction',
            options={'verbose_name': 'Declare faction the winner', 'verbose_name_plural': 'Declare faction the winner actions'},
        ),
        migrations.AlterModelOptions(
            name='declarekillerthewinnerkillaction',
            options={'verbose_name': 'Declare killer the winner', 'verbose_name_plural': 'Declare killer the winner actions'},
        ),
    ]
