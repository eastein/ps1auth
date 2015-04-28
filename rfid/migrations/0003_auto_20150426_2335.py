# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rfid', '0002_auto_20150309_1454'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEvent',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='WebUnlock',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length='255')),
                ('resource', models.ForeignKey(to='rfid.Resource')),
            ],
        ),
        migrations.CreateModel(
            name='ButtonPressLogEvent',
            fields=[
                ('logevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='rfid.LogEvent', serialize=False, primary_key=True)),
            ],
            bases=('rfid.logevent',),
        ),
        migrations.CreateModel(
            name='RFIDAccessLogEvent',
            fields=[
                ('logevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='rfid.LogEvent', serialize=False, primary_key=True)),
            ],
            bases=('rfid.logevent',),
        ),
        migrations.AddField(
            model_name='logevent',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
