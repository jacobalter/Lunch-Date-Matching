# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-14 15:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matchingApp', '0003_auto_20170414_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busyat',
            name='userid',
            field=models.ForeignKey(db_column='userid', on_delete=django.db.models.deletion.DO_NOTHING, to='matchingApp.Person'),
        ),
        migrations.AlterField(
            model_name='friends',
            name='user1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user1', to='matchingApp.Person'),
        ),
        migrations.AlterField(
            model_name='friends',
            name='user2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user2', to='matchingApp.Person'),
        ),
    ]
