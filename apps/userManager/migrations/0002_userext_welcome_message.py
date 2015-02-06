# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userManager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userext',
            name='welcome_message',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
