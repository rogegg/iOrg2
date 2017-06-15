# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-13 17:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datareader', '0007_auto_20170608_1801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='concept',
            name='sub_variable',
        ),
        migrations.RemoveField(
            model_name='concept',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='concept',
            name='topic',
        ),
        migrations.RemoveField(
            model_name='concept',
            name='variable',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='subtopics_id',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='topic_id',
        ),
        migrations.AddField(
            model_name='concept',
            name='subtopic',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='datareader.SubTopic'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subtopic',
            name='topic',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='datareader.Topic'),
            preserve_default=False,
        ),
    ]
