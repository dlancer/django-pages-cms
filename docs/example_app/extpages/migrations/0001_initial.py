# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import embed_video.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PageVideoContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100, verbose_name='Type', db_index=True)),
                ('language', models.CharField(default=b'en', max_length=5)),
                ('sid', models.CharField(unique=True, max_length=200)),
                ('name', models.CharField(unique=True, max_length=200, blank=True)),
                ('is_extended', models.BooleanField(default=True, verbose_name='Extended?')),
                ('comment', models.CharField(max_length=250, blank=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created')),
                ('date_updated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated')),
                ('video', embed_video.fields.EmbedVideoField(blank=True)),
                ('title', models.CharField(max_length=160, blank=True)),
                ('description', models.TextField(max_length=160, blank=True)),
                ('created_by', models.ForeignKey(related_name='extpages_pagevideocontent_creator', to=settings.AUTH_USER_MODEL, null=True)),
                ('page', models.ForeignKey(verbose_name='Page', to='pages.Page')),
                ('updated_by', models.ForeignKey(related_name='extpages_pagevideocontent_editor', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Video',
                'verbose_name_plural': 'Video',
            },
            bases=(models.Model,),
        ),
    ]
