# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rfid', '0004_auto_20150426_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webunlock',
            name='resource',
            field=models.OneToOneField(to='rfid.Resource'),
        ),
    ]
