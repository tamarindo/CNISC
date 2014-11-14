# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('consumer_key', models.CharField(max_length=400, null=True, verbose_name='consumer_key', blank=True)),
                ('consumer_secret', models.CharField(max_length=400, null=True, verbose_name='consumer_secret', blank=True)),
                ('nombre', models.CharField(max_length=30, verbose_name='nombre')),
                ('provedor', models.CharField(max_length=1, verbose_name='Provedores', choices=[(b'Facebook', b'Facebook'), (b'Twitter', b'Twitter')])),
                ('callback_url', models.CharField(max_length=500, verbose_name='callback url')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CuentaSocial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('uid', models.CharField(max_length=400, null=True, verbose_name='uid', blank=True)),
                ('select', models.BooleanField(default=False)),
                ('app', models.ForeignKey(verbose_name='App', to='oauthSocial.App')),
                ('user', models.ForeignKey(verbose_name='usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TokenSocial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(max_length=500, verbose_name='token')),
                ('token_secreto', models.CharField(max_length=500, verbose_name='token secreto')),
                ('fecha_expiracion', models.DateTimeField(verbose_name='fecha expiracion')),
                ('cuenta', models.ForeignKey(verbose_name='CuentaSocial', to='oauthSocial.CuentaSocial')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
