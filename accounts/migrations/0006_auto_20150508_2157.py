# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20150425_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ps1group',
            name='dn',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
