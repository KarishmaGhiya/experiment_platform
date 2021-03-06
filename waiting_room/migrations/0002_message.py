# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-11 19:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('waiting_room', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('wait_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='waiting_room.WaitRoom')),
            ],
        ),
    ]
