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
            name='Graduate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('program', models.CharField(max_length=50, null=True, verbose_name='Egresado del programa de', blank=True)),
                ('job', models.CharField(max_length=50, null=True, verbose_name='Empleo', blank=True)),
                ('scope', models.CharField(max_length=20, null=True, verbose_name='Ambito laboral', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20, null=True, verbose_name='Nombre del tipo del perfil', blank=True)),
                ('abbr', models.CharField(max_length=5, null=True, verbose_name='Abreviacion del nombre del perfil', blank=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('semester', models.IntegerField(null=True, verbose_name='Semestre', blank=True)),
                ('academic_state', models.CharField(max_length=50, null=True, verbose_name='Estado academico', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserExt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('gender', models.CharField(blank=True, max_length=1, null=True, verbose_name='Genero', choices=[(b'M', 'Masculino'), (b'F', 'Femenino'), (b'N', 'No definido')])),
                ('phone', models.CharField(max_length=25, null=True, verbose_name='Telefono', blank=True)),
                ('mobile', models.CharField(max_length=25, null=True, verbose_name='Celular', blank=True)),
                ('address', models.CharField(max_length=60, null=True, verbose_name='direccion', blank=True)),
                ('city', models.CharField(max_length=60, null=True, verbose_name='ciudad', blank=True)),
                ('province', models.CharField(max_length=60, null=True, verbose_name='estado', blank=True)),
                ('country', models.CharField(max_length=60, null=True, verbose_name='pais', blank=True)),
                ('date_born', models.DateField(null=True, verbose_name='Fecha de nacimiento', blank=True)),
                ('profile', models.ForeignKey(verbose_name='Perfil', to='userManager.Profile')),
                ('user', models.OneToOneField(verbose_name='Usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='student',
            name='UserExt',
            field=models.OneToOneField(verbose_name='UserExt', to='userManager.UserExt'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='graduate',
            name='UserExt',
            field=models.OneToOneField(verbose_name='UserExt', to='userManager.UserExt'),
            preserve_default=True,
        ),
    ]
