# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member_management', '0010_auto_20150309_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailrecord',
            name='from_email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='emailrecord',
            name='reply_to_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='emailrecord',
            name='to_email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='from_email',
            field=models.EmailField(verbose_name='From', max_length=254),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='reply_to_email',
            field=models.EmailField(blank=True, verbose_name='Reply-To', max_length=254),
        ),
        migrations.AlterField(
            model_name='paypal',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(null=True, blank=True, max_length=254),
        ),
    ]
