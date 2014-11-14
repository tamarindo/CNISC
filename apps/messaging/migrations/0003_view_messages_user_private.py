# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_remove_view_messages_user_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='view_messages_user',
            name='private',
            field=models.BooleanField(default=False, verbose_name='es privado'),
            preserve_default=True,
        ),
    ]
