# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0006_auto_20150508_2157'),
        ('rfid', '0002_auto_20150309_1454'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEvent',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WebUnlock',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('url', models.URLField()),
            ],
        ),
        migrations.RemoveField(
            model_name='adgroupresource',
            name='ad_group',
        ),
        migrations.AddField(
            model_name='adgroupresource',
            name='group',
            field=models.ForeignKey(to='accounts.PS1Group', default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resource',
            name='display_name',
            field=models.CharField(max_length=160, default=''),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ButtonPressLogEvent',
            fields=[
                ('logevent_ptr', models.OneToOneField(serialize=False, auto_created=True, to='rfid.LogEvent', parent_link=True, primary_key=True)),
                ('ip_address', models.GenericIPAddressField()),
            ],
            bases=('rfid.logevent',),
        ),
        migrations.CreateModel(
            name='RFIDAccessLogEvent',
            fields=[
                ('logevent_ptr', models.OneToOneField(serialize=False, auto_created=True, to='rfid.LogEvent', parent_link=True, primary_key=True)),
                ('original_key', models.CharField(max_length=12)),
                ('rfid_number', models.ForeignKey(to='rfid.RFIDNumber')),
            ],
            bases=('rfid.logevent',),
        ),
        migrations.AddField(
            model_name='webunlock',
            name='resource',
            field=models.OneToOneField(to='rfid.Resource'),
        ),
        migrations.AddField(
            model_name='logevent',
            name='resource',
            field=models.ForeignKey(to='rfid.Resource'),
        ),
        migrations.AddField(
            model_name='logevent',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
