# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oauthSocial', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tokensocial',
            name='fecha_expiracion',
        ),
        migrations.AlterField(
            model_name='app',
            name='provedor',
            field=models.CharField(max_length=10, verbose_name='Provedores', choices=[(b'Facebook', b'Facebook'), (b'Twitter', b'Twitter')]),
        ),
    ]
