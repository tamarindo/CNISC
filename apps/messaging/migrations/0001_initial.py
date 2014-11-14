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
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('data', models.FileField(max_length=200, upload_to=b'adjuntos')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('subject', models.CharField(max_length=120, null=True, verbose_name='Asunto', blank=True)),
                ('content', models.TextField(null=True, verbose_name='Mensaje', blank=True)),
                ('sender', models.ForeignKey(verbose_name='Remitente', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='View_Messages_User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('seen', models.BooleanField(default=False, verbose_name='Visto')),
                ('private', models.BooleanField(default=False, verbose_name='es privado')),
                ('seen_date', models.DateTimeField(null=True, verbose_name='Fecha', blank=True)),
                ('message', models.ForeignKey(verbose_name='Mensaje', to='messaging.Message')),
                ('user', models.ForeignKey(verbose_name='Usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='attachment',
            name='message',
            field=models.ForeignKey(verbose_name='Mensaje', to='messaging.Message'),
            preserve_default=True,
        ),
    ]
