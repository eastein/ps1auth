# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_ps1group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ps1group',
            options={'verbose_name': 'PS1 Group'},
        ),
        migrations.AddField(
            model_name='ps1group',
            name='display_name',
            field=models.CharField(max_length=255, default=''),
            preserve_default=False,
        ),
    ]
