# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import encrypted_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('assassins', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=encrypted_fields.fields.EncryptedCharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=encrypted_fields.fields.EncryptedCharField(default='', max_length=40),
            preserve_default=False,
        ),
    ]
