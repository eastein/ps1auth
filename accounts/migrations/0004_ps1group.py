# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20150424_2257'),
    ]

    operations = [
        migrations.CreateModel(
            name='PS1Group',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('dn', models.CharField(max_length=255)),
            ],
        ),
    ]
