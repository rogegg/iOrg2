# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-13 16:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datareader', '0008_auto_20170613_1728'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('answer', models.CharField(max_length=300)),
                ('options', models.CharField(max_length=300)),
                ('reason', models.CharField(max_length=300)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datareader.Topic')),
            ],
        ),
    ]