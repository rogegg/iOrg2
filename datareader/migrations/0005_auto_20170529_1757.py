# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-29 17:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datareader', '0004_auto_20170529_1724'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='subject_code',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='subject_name',
            new_name='name',
        ),
    ]
